"""Tests for tf_cli.init_new module."""
from __future__ import annotations

import os
from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.unit

from tf_cli import init_new


class TestReadRootFile:
    """Tests for read_root_file function."""

    def test_reads_file_content(self, tmp_path: Path) -> None:
        """Should read and return file content."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("  hello world  \n")
        result = init_new.read_root_file(test_file)
        assert result == "hello world"

    def test_returns_empty_on_missing_file(self, tmp_path: Path) -> None:
        """Should return empty string when file doesn't exist."""
        result = init_new.read_root_file(tmp_path / "nonexistent.txt")
        assert result == ""

    def test_returns_empty_on_error(self, tmp_path: Path) -> None:
        """Should return empty string on any error."""
        with mock.patch("pathlib.Path.read_text", side_effect=PermissionError()):
            result = init_new.read_root_file(tmp_path / "test.txt")
            assert result == ""


class TestFindRepoRoot:
    """Tests for find_repo_root function."""

    def test_uses_env_var(self, tmp_path: Path) -> None:
        """Should use TF_REPO_ROOT environment variable."""
        with mock.patch.dict(os.environ, {"TF_REPO_ROOT": str(tmp_path)}):
            result = init_new.find_repo_root()
            assert result == tmp_path

    def test_ignores_env_var_if_path_doesnt_exist(self, tmp_path: Path) -> None:
        """Should ignore env var if path doesn't exist."""
        nonexistent = tmp_path / "nonexistent"
        # Clear any pre-existing env var and mock the cwd to avoid finding actual repo root
        with mock.patch.dict(os.environ, {"TF_REPO_ROOT": str(nonexistent)}, clear=True):
            with mock.patch("tf_cli.init_new.Path.cwd", return_value=tmp_path):
                with mock.patch("pathlib.Path.home", return_value=tmp_path / "home"):
                    result = init_new.find_repo_root()
                    assert result is None

    def test_uses_cli_root_file_in_cwd(self, tmp_path: Path) -> None:
        """Should find and use .tf/cli-root in cwd."""
        (tmp_path / ".tf").mkdir()
        cli_root = tmp_path / ".tf/cli-root"
        cli_root.write_text(str(tmp_path / "repo"))
        (tmp_path / "repo").mkdir()

        with mock.patch("tf_cli.init_new.Path.cwd", return_value=tmp_path):
            result = init_new.find_repo_root()
            assert result == tmp_path / "repo"

    def test_uses_cli_root_file_in_parent(self, tmp_path: Path) -> None:
        """Should find .tf/cli-root in parent directories."""
        (tmp_path / ".tf").mkdir()
        cli_root = tmp_path / ".tf/cli-root"
        cli_root.write_text(str(tmp_path / "repo"))
        (tmp_path / "repo").mkdir()

        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)

        with mock.patch("tf_cli.init_new.Path.cwd", return_value=subdir):
            result = init_new.find_repo_root()
            assert result == tmp_path / "repo"

    def test_uses_home_cli_root_file(self, tmp_path: Path) -> None:
        """Should use ~/.tf/cli-root as fallback."""
        home_tf = tmp_path / "home" / ".tf"
        home_tf.mkdir(parents=True)
        cli_root = home_tf / "cli-root"
        cli_root.write_text(str(tmp_path / "repo"))
        (tmp_path / "repo").mkdir()

        with mock.patch("pathlib.Path.home", return_value=tmp_path / "home"):
            with mock.patch("tf_cli.init_new.Path.cwd", return_value=tmp_path):
                result = init_new.find_repo_root()
                assert result == tmp_path / "repo"

    def test_returns_none_when_nothing_found(self, tmp_path: Path) -> None:
        """Should return None when no repo root found."""
        with mock.patch("tf_cli.init_new.Path.cwd", return_value=tmp_path):
            with mock.patch("pathlib.Path.home", return_value=tmp_path / "home"):
                result = init_new.find_repo_root()
                assert result is None


class TestRawBaseFromSource:
    """Tests for raw_base_from_source function."""

    def test_github_url_with_git_prefix(self) -> None:
        """Should handle git+https:// GitHub URLs."""
        result = init_new.raw_base_from_source("git+https://github.com/owner/repo")
        assert result == "https://raw.githubusercontent.com/owner/repo/main"

    def test_github_url_with_ref(self) -> None:
        """Should extract ref from URL."""
        result = init_new.raw_base_from_source("https://github.com/owner/repo@develop")
        assert result == "https://raw.githubusercontent.com/owner/repo/develop"

    def test_github_url_with_dotgit(self) -> None:
        """Should handle .git suffix."""
        result = init_new.raw_base_from_source("https://github.com/owner/repo.git")
        assert result == "https://raw.githubusercontent.com/owner/repo/main"

    def test_returns_none_for_non_github(self) -> None:
        """Should return None for non-GitHub URLs."""
        result = init_new.raw_base_from_source("https://gitlab.com/owner/repo")
        assert result is None

    def test_returns_none_for_invalid_url(self) -> None:
        """Should return None for invalid URLs."""
        result = init_new.raw_base_from_source("not-a-url")
        assert result is None


class TestEnsureFile:
    """Tests for ensure_file function."""

    def test_skips_if_file_exists(self, tmp_path: Path) -> None:
        """Should skip if file already exists."""
        dest = tmp_path / "test.txt"
        dest.write_text("existing")

        init_new.ensure_file(dest, "config/test.txt", None)

        # File should not be modified
        assert dest.read_text() == "existing"

    def test_copies_from_repo_root(self, tmp_path: Path) -> None:
        """Should copy from repo root when available."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        source = repo_root / "config/test.txt"
        source.parent.mkdir(parents=True)
        source.write_text("from repo")

        dest = tmp_path / "dest.txt"
        init_new.ensure_file(dest, "config/test.txt", repo_root)

        assert dest.exists()
        assert dest.read_text() == "from repo"

    def test_downloads_when_no_repo_root(self, tmp_path: Path) -> None:
        """Should download when no repo root available."""
        dest = tmp_path / "dest.txt"

        mock_response = mock.Mock()
        mock_response.read.return_value = b"downloaded content"
        mock_context = mock.Mock()
        mock_context.__enter__ = mock.Mock(return_value=mock_response)
        mock_context.__exit__ = mock.Mock(return_value=False)

        with mock.patch("urllib.request.urlopen", return_value=mock_context):
            with mock.patch.object(init_new, "resolve_raw_base", return_value="https://example.com"):
                init_new.ensure_file(dest, "file.txt", None)

        assert dest.exists()
        assert dest.read_text() == "downloaded content"

    def test_handles_download_error(self, tmp_path: Path, capsys) -> None:
        """Should handle download errors gracefully."""
        dest = tmp_path / "dest.txt"

        with mock.patch("urllib.request.urlopen", side_effect=Exception("Network error")):
            with mock.patch.object(init_new, "resolve_raw_base", return_value="https://example.com"):
                # Should not raise
                init_new.ensure_file(dest, "file.txt", None)

        # File should not exist after failed download
        assert not dest.exists()


class TestInitProject:
    """Tests for init_project function."""

    def test_creates_tf_directory_structure(self, tmp_path: Path) -> None:
        """Should create .tf directory structure."""
        with mock.patch.object(init_new, "ensure_file"):
            result = init_new.init_project(tmp_path)

        assert result == 0
        assert (tmp_path / ".tf").exists()
        assert (tmp_path / ".tf/config").exists()
        assert (tmp_path / ".tf/scripts").exists()
        assert (tmp_path / ".tf/knowledge").exists()
        assert (tmp_path / ".tf/ralph").exists()

    def test_calls_ensure_file_for_config_files(self, tmp_path: Path) -> None:
        """Should call ensure_file for config files."""
        with mock.patch.object(init_new, "ensure_file") as mock_ensure:
            init_new.init_project(tmp_path)

            mock_ensure.assert_any_call(
                tmp_path / ".tf/config/settings.json",
                "config/settings.json",
                mock.ANY
            )
            mock_ensure.assert_any_call(
                tmp_path / ".tf/scripts/tf_config.py",
                "scripts/tf_config.py",
                mock.ANY
            )


class TestMain:
    """Tests for main function."""

    def test_rejects_global_flag(self, capsys) -> None:
        """Should reject --global flag."""
        result = init_new.main(["--global"])
        assert result == 1
        captured = capsys.readouterr()
        assert "project-local" in captured.err

    def test_uses_project_arg(self, tmp_path: Path) -> None:
        """Should use --project argument."""
        project_path = tmp_path / "myproject"

        with mock.patch.object(init_new, "init_project", return_value=0) as mock_init:
            result = init_new.main(["--project", str(project_path)])

        assert result == 0
        mock_init.assert_called_once_with(project_path)

    def test_uses_cwd_when_no_project_arg(self, tmp_path: Path) -> None:
        """Should use current directory when no --project."""
        with mock.patch("tf_cli.init_new.Path.cwd", return_value=tmp_path):
            with mock.patch.object(init_new, "init_project", return_value=0) as mock_init:
                result = init_new.main([])

        assert result == 0
        mock_init.assert_called_once_with(tmp_path)

    def test_expands_user_in_project_path(self, tmp_path: Path) -> None:
        """Should expand ~ in project path."""
        with mock.patch("pathlib.Path.expanduser", return_value=tmp_path) as mock_expand:
            with mock.patch.object(init_new, "init_project", return_value=0):
                init_new.main(["--project", "~/project"])

        mock_expand.assert_called()
