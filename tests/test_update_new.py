"""Tests for tf_cli.update_new module."""
from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.unit

from tf_cli import update_new


class TestDownload:
    """Tests for download function."""

    def test_downloads_file_successfully(self, tmp_path: Path) -> None:
        """Should download file successfully."""
        dest = tmp_path / "downloaded.txt"

        mock_response = mock.Mock()
        mock_response.read.return_value = b"downloaded content"
        mock_context = mock.Mock()
        mock_context.__enter__ = mock.Mock(return_value=mock_response)
        mock_context.__exit__ = mock.Mock(return_value=False)

        with mock.patch("urllib.request.urlopen", return_value=mock_context):
            result = update_new.download("https://example.com/file.txt", dest)

        assert result is True
        assert dest.exists()
        assert dest.read_text() == "downloaded content"

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        """Should create parent directories."""
        dest = tmp_path / "nested" / "deep" / "file.txt"

        mock_response = mock.Mock()
        mock_response.read.return_value = b"content"
        mock_context = mock.Mock()
        mock_context.__enter__ = mock.Mock(return_value=mock_response)
        mock_context.__exit__ = mock.Mock(return_value=False)

        with mock.patch("urllib.request.urlopen", return_value=mock_context):
            result = update_new.download("https://example.com/file.txt", dest)

        assert result is True
        assert dest.exists()

    def test_returns_false_on_error(self, tmp_path: Path) -> None:
        """Should return False on download error."""
        dest = tmp_path / "file.txt"

        with mock.patch("urllib.request.urlopen", side_effect=Exception("Network error")):
            result = update_new.download("https://example.com/file.txt", dest)

        assert result is False
        assert not dest.exists()


class TestParseManifest:
    """Tests for parse_manifest function."""

    def test_parses_valid_entries(self, tmp_path: Path) -> None:
        """Should parse valid manifest entries."""
        manifest = tmp_path / "manifest.txt"
        manifest.write_text("""
agents/test.md
skills/test/
prompts/test.md
# This is a comment
   agents/spaces.md

other/file.txt
""")

        result = update_new.parse_manifest(manifest)
        assert "agents/test.md" in result
        assert "skills/test/" in result
        assert "prompts/test.md" in result
        assert "agents/spaces.md" in result
        assert "other/file.txt" not in result  # Doesn't start with valid prefix
        assert "# This is a comment" not in result

    def test_returns_empty_on_empty_file(self, tmp_path: Path) -> None:
        """Should return empty list for empty file."""
        manifest = tmp_path / "manifest.txt"
        manifest.write_text("")

        result = update_new.parse_manifest(manifest)
        assert result == []

    def test_skips_comments_and_empty_lines(self, tmp_path: Path) -> None:
        """Should skip comments and empty lines."""
        manifest = tmp_path / "manifest.txt"
        manifest.write_text("""
# Comment 1
agents/test.md

# Comment 2
   
prompts/test.md
""")

        result = update_new.parse_manifest(manifest)
        assert result == ["agents/test.md", "prompts/test.md"]


class TestResolveTargetBase:
    """Tests for resolve_target_base function."""

    def test_uses_project_arg(self, tmp_path: Path) -> None:
        """Should use project argument."""
        args = mock.Mock(project=str(tmp_path / "project"), global_install=False)
        result = update_new.resolve_target_base(args)
        assert result == tmp_path / "project" / ".pi"

    def test_uses_global_when_flag_set(self, tmp_path: Path) -> None:
        """Should use global path when --global flag set."""
        with mock.patch("tf_cli.update_new.Path.home", return_value=tmp_path / "home"):
            args = mock.Mock(project=None, global_install=True)
            result = update_new.resolve_target_base(args)
            assert result == tmp_path / "home" / ".pi" / "agent"

    def test_uses_cwd_pi_when_exists(self, tmp_path: Path) -> None:
        """Should use cwd/.pi when it exists."""
        (tmp_path / ".pi").mkdir()
        with mock.patch("tf_cli.update_new.Path.cwd", return_value=tmp_path):
            args = mock.Mock(project=None, global_install=False)
            result = update_new.resolve_target_base(args)
            assert result == tmp_path / ".pi"

    def test_falls_back_to_global(self, tmp_path: Path) -> None:
        """Should fall back to global when no .pi in cwd."""
        with mock.patch("tf_cli.update_new.Path.cwd", return_value=tmp_path):
            with mock.patch("tf_cli.update_new.Path.home", return_value=tmp_path / "home"):
                args = mock.Mock(project=None, global_install=False)
                result = update_new.resolve_target_base(args)
                assert result == tmp_path / "home" / ".pi" / "agent"


class TestPromptYesNo:
    """Tests for prompt_yes_no function."""

    def test_yes_input_with_default_yes(self) -> None:
        """Should return True for 'y' input with default_yes=True."""
        with mock.patch("builtins.input", return_value="y"):
            result = update_new.prompt_yes_no("Continue?", default_yes=True)
            assert result is True

    def test_yes_input_with_default_no(self) -> None:
        """Should return True for 'y' input with default_yes=False."""
        with mock.patch("builtins.input", return_value="y"):
            result = update_new.prompt_yes_no("Continue?", default_yes=False)
            assert result is True

    def test_no_input_with_default_yes(self) -> None:
        """Should return False for 'n' input with default_yes=True."""
        with mock.patch("builtins.input", return_value="n"):
            result = update_new.prompt_yes_no("Continue?", default_yes=True)
            assert result is False

    def test_no_input_with_default_no(self) -> None:
        """Should return False for 'n' input with default_yes=False."""
        with mock.patch("builtins.input", return_value="n"):
            result = update_new.prompt_yes_no("Continue?", default_yes=False)
            assert result is False

    def test_empty_input_uses_default_yes(self) -> None:
        """Should return True for empty input with default_yes=True."""
        with mock.patch("builtins.input", return_value=""):
            result = update_new.prompt_yes_no("Continue?", default_yes=True)
            assert result is True

    def test_empty_input_uses_default_no(self) -> None:
        """Should return False for empty input with default_yes=False."""
        with mock.patch("builtins.input", return_value=""):
            result = update_new.prompt_yes_no("Continue?", default_yes=False)
            assert result is False

    def test_case_insensitive_yes(self) -> None:
        """Should handle 'Y' input case-insensitively."""
        with mock.patch("builtins.input", return_value="Y"):
            result = update_new.prompt_yes_no("Continue?", default_yes=False)
            assert result is True

    def test_yes_with_extra_whitespace(self) -> None:
        """Should handle 'yes' with extra whitespace."""
        with mock.patch("builtins.input", return_value="  yes  "):
            result = update_new.prompt_yes_no("Continue?", default_yes=False)
            assert result is True


class TestUpdateAssets:
    """Tests for update_assets function."""

    def test_downloads_new_files(self, tmp_path: Path) -> None:
        """Should download new files."""
        target_base = tmp_path / ".pi"
        target_base.mkdir(parents=True)

        def mock_download(url, dest):
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text("content")
            return True

        with mock.patch("tf_cli.update_new.download", side_effect=mock_download):
            with mock.patch("tf_cli.update_new.parse_manifest", return_value=["agents/test.md"]):
                with mock.patch("tf_cli.update_new.prompt_yes_no", return_value=True):
                    result = update_new.update_assets(target_base)

        assert result == 0

    def test_handles_no_new_files(self, tmp_path: Path) -> None:
        """Should handle when no new files available."""
        (tmp_path / ".pi" / "agents").mkdir(parents=True)
        existing_file = tmp_path / ".pi" / "agents" / "test.md"
        existing_file.write_text("exists")

        with mock.patch("tf_cli.update_new.download"):
            with mock.patch("tf_cli.update_new.parse_manifest", return_value=["agents/test.md"]):
                with mock.patch("tf_cli.update_new.prompt_yes_no", side_effect=[False, False]):
                    result = update_new.update_assets(tmp_path / ".pi")

        assert result == 0

    def test_returns_error_on_manifest_download_failure(self, tmp_path: Path) -> None:
        """Should return 1 when manifest download fails."""
        with mock.patch("tf_cli.update_new.download", return_value=False):
            result = update_new.update_assets(tmp_path / ".pi")

        assert result == 1


class TestBuildParser:
    """Tests for build_parser function."""

    def test_parser_has_project_option(self) -> None:
        """Parser should have --project option."""
        parser = update_new.build_parser()
        args = parser.parse_args(["--project", "/some/path"])
        assert args.project == "/some/path"

    def test_parser_has_global_flag(self) -> None:
        """Parser should have --global flag."""
        parser = update_new.build_parser()
        args = parser.parse_args(["--global"])
        assert args.global_install is True


class TestMain:
    """Tests for main function."""

    def test_runs_update_successfully(self, tmp_path: Path) -> None:
        """Should run update and return result."""
        (tmp_path / ".pi" / "agents").mkdir(parents=True)

        with mock.patch("tf_cli.update_new.update_assets", return_value=0) as mock_update:
            with mock.patch("tf_cli.update_new.Path.cwd", return_value=tmp_path):
                result = update_new.main([])
                assert result == 0

    def test_creates_target_base_if_missing(self, tmp_path: Path) -> None:
        """Should create target base directory if it doesn't exist."""
        target_base = tmp_path / "new" / "path"

        with mock.patch("tf_cli.update_new.resolve_target_base", return_value=target_base):
            with mock.patch("tf_cli.update_new.update_assets", return_value=0):
                update_new.main([])

        assert target_base.exists()

    def test_parses_args(self, tmp_path: Path) -> None:
        """Should parse command line arguments."""
        project_path = tmp_path / "project"
        project_path.mkdir(parents=True)

        with mock.patch("tf_cli.update_new.update_assets") as mock_update:
            update_new.main(["--project", str(project_path)])
            mock_update.assert_called_once()
