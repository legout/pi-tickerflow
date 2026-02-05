"""Tests for tf_cli.sync_new module."""
from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.unit

from tf_cli import sync_new


class TestReadJson:
    """Tests for read_json function."""

    def test_reads_valid_json(self, tmp_path: Path) -> None:
        """Should read and parse valid JSON."""
        json_file = tmp_path / "config.json"
        json_file.write_text(json.dumps({"key": "value", "number": 42}))

        result = sync_new.read_json(json_file)
        assert result == {"key": "value", "number": 42}

    def test_returns_empty_dict_on_missing_file(self, tmp_path: Path) -> None:
        """Should return empty dict when file doesn't exist."""
        result = sync_new.read_json(tmp_path / "nonexistent.json")
        assert result == {}

    def test_returns_empty_dict_on_invalid_json(self, tmp_path: Path) -> None:
        """Should return empty dict when JSON is invalid."""
        json_file = tmp_path / "config.json"
        json_file.write_text("not valid json")

        result = sync_new.read_json(json_file)
        assert result == {}


class TestMerge:
    """Tests for merge function."""

    def test_merges_simple_dicts(self) -> None:
        """Should merge two simple dicts."""
        a = {"key1": "value1"}
        b = {"key2": "value2"}
        result = sync_new.merge(a, b)
        assert result == {"key1": "value1", "key2": "value2"}

    def test_b_overrides_a(self) -> None:
        """Values in b should override values in a."""
        a = {"key": "value_a"}
        b = {"key": "value_b"}
        result = sync_new.merge(a, b)
        assert result == {"key": "value_b"}

    def test_deep_merge_nested_dicts(self) -> None:
        """Should recursively merge nested dicts."""
        a = {"outer": {"inner1": "value1"}}
        b = {"outer": {"inner2": "value2"}}
        result = sync_new.merge(a, b)
        assert result == {"outer": {"inner1": "value1", "inner2": "value2"}}

    def test_nested_override(self) -> None:
        """Should override nested values."""
        a = {"outer": {"inner": "value_a"}}
        b = {"outer": {"inner": "value_b"}}
        result = sync_new.merge(a, b)
        assert result == {"outer": {"inner": "value_b"}}

    def test_b_non_dict_overrides_a_dict(self) -> None:
        """Non-dict in b should override dict in a."""
        a = {"key": {"nested": "value"}}
        b = {"key": "simple_value"}
        result = sync_new.merge(a, b)
        assert result == {"key": "simple_value"}


class TestResolveProjectRoot:
    """Tests for resolve_project_root function."""

    def test_returns_parent_when_path_ends_with_pi(self, tmp_path: Path) -> None:
        """Should return parent when path ends with .pi."""
        pi_path = tmp_path / "project" / ".pi"
        result = sync_new.resolve_project_root(pi_path)
        assert result == tmp_path / "project"

    def test_returns_cwd_when_path_does_not_end_with_pi(self, tmp_path: Path) -> None:
        """Should return cwd when path doesn't end with .pi."""
        with mock.patch("tf_cli.sync_new.Path.cwd", return_value=tmp_path):
            result = sync_new.resolve_project_root(tmp_path / "other")
            assert result == tmp_path


class TestResolveProjectConfig:
    """Tests for resolve_project_config function."""

    def test_returns_correct_config_path(self, tmp_path: Path) -> None:
        """Should return correct settings.json path."""
        pi_path = tmp_path / "project" / ".pi"
        result = sync_new.resolve_project_config(pi_path)
        assert result == tmp_path / "project" / ".tf" / "config" / "settings.json"


class TestLoadWorkflowConfig:
    """Tests for load_workflow_config function."""

    def test_merges_global_and_project_config(self, tmp_path: Path) -> None:
        """Should merge global and project config."""
        global_config = tmp_path / "global" / ".tf" / "config" / "settings.json"
        global_config.parent.mkdir(parents=True)
        global_config.write_text(json.dumps({"global_key": "global_value", "shared": "from_global"}))

        project_config = tmp_path / "project" / ".tf" / "config" / "settings.json"
        project_config.parent.mkdir(parents=True)
        project_config.write_text(json.dumps({"project_key": "project_value", "shared": "from_project"}))

        with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "global"):
            with mock.patch("tf_cli.sync_new.resolve_project_config", return_value=project_config):
                result = sync_new.load_workflow_config(tmp_path / "project" / ".pi", ignore_project=False)

        assert result["global_key"] == "global_value"
        assert result["project_key"] == "project_value"
        assert result["shared"] == "from_project"  # Project overrides global

    def test_ignores_project_when_ignore_project_true(self, tmp_path: Path) -> None:
        """Should ignore project config when ignore_project is True."""
        global_config = tmp_path / "global" / ".tf" / "config" / "settings.json"
        global_config.parent.mkdir(parents=True)
        global_config.write_text(json.dumps({"key": "global_value"}))

        with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "global"):
            result = sync_new.load_workflow_config(tmp_path / "project" / ".pi", ignore_project=True)

        assert result["key"] == "global_value"


class TestResolveSyncBase:
    """Tests for resolve_sync_base function."""

    def test_returns_base_when_agents_dir_exists(self, tmp_path: Path) -> None:
        """Should return base when agents directory exists."""
        (tmp_path / "agents").mkdir()
        result = sync_new.resolve_sync_base(tmp_path)
        assert result == tmp_path

    def test_returns_base_when_prompts_dir_exists(self, tmp_path: Path) -> None:
        """Should return base when prompts directory exists."""
        (tmp_path / "prompts").mkdir()
        result = sync_new.resolve_sync_base(tmp_path)
        assert result == tmp_path

    def test_falls_back_to_global_base(self, tmp_path: Path) -> None:
        """Should fall back to global base when no local agents/prompts."""
        global_base = tmp_path / "global" / ".pi" / "agent"
        (global_base / "agents").mkdir(parents=True)

        with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "global"):
            result = sync_new.resolve_sync_base(tmp_path / "project")
            assert result == global_base

    def test_returns_base_when_nothing_exists(self, tmp_path: Path) -> None:
        """Should return base when nothing exists."""
        with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "home"):
            result = sync_new.resolve_sync_base(tmp_path / "project")
            assert result == tmp_path / "project"


class TestResolveMetaModel:
    """Tests for resolve_meta_model function."""

    def test_resolves_from_meta_models(self) -> None:
        """Should resolve from metaModels directly."""
        config = {"metaModels": {"fast": {"model": "gpt-4", "thinking": "low"}}}
        result = sync_new.resolve_meta_model(config, "fast")
        assert result == {"model": "gpt-4", "thinking": "low"}

    def test_resolves_via_agents_map(self) -> None:
        """Should resolve via agents map."""
        config = {
            "metaModels": {"worker": {"model": "gpt-4", "thinking": "medium"}},
            "agents": {"my_agent": "worker"}
        }
        result = sync_new.resolve_meta_model(config, "my_agent")
        assert result == {"model": "gpt-4", "thinking": "medium"}

    def test_resolves_via_prompts_map(self) -> None:
        """Should resolve via prompts map."""
        config = {
            "metaModels": {"default": {"model": "gpt-3.5", "thinking": "high"}},
            "prompts": {"my_prompt": "default"}
        }
        result = sync_new.resolve_meta_model(config, "my_prompt")
        assert result == {"model": "gpt-3.5", "thinking": "high"}

    def test_returns_defaults_when_not_found(self) -> None:
        """Should return defaults when name not found."""
        config = {}
        result = sync_new.resolve_meta_model(config, "unknown")
        # The module uses version.get_version() as default model, which returns actual version
        assert result["model"] is not None
        assert result["thinking"] == "medium"


class TestUpdateAgentFrontmatter:
    """Tests for update_agent_frontmatter function."""

    def test_updates_existing_frontmatter(self, tmp_path: Path) -> None:
        """Should update existing frontmatter values."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
model: old-model
thinking: low
---
# Agent
""")
        config = {"metaModels": {"agent": {"model": "new-model", "thinking": "high"}}, "agents": {"agent": "agent"}}

        result = sync_new.update_agent_frontmatter(agent_file, config, "agent")

        assert result is True
        content = agent_file.read_text()
        assert "model: new-model" in content
        assert "thinking: high" in content

    def test_adds_missing_frontmatter_fields(self, tmp_path: Path) -> None:
        """Should add missing frontmatter fields."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
model: old-model
---
# Agent
""")
        config = {"metaModels": {"agent": {"model": "new-model", "thinking": "high"}}, "agents": {"agent": "agent"}}

        result = sync_new.update_agent_frontmatter(agent_file, config, "agent")

        assert result is True
        content = agent_file.read_text()
        assert "model: new-model" in content
        assert "thinking: high" in content

    def test_returns_false_when_no_change(self, tmp_path: Path) -> None:
        """Should return False when no changes needed."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("""---
model: gpt-4
thinking: medium
---
# Agent
""")
        config = {"metaModels": {"agent": {"model": "gpt-4", "thinking": "medium"}}, "agents": {"agent": "agent"}}

        result = sync_new.update_agent_frontmatter(agent_file, config, "agent")

        assert result is False

    def test_handles_file_without_frontmatter(self, tmp_path: Path) -> None:
        """Should handle files without frontmatter."""
        agent_file = tmp_path / "agent.md"
        agent_file.write_text("# Agent\nContent")

        config = {"metaModels": {"agent": {"model": "gpt-4", "thinking": "medium"}}, "agents": {"agent": "agent"}}

        # Should not raise
        result = sync_new.update_agent_frontmatter(agent_file, config, "agent")
        # No frontmatter to update, so no change
        assert result is False


class TestSyncModels:
    """Tests for sync_models function."""

    def test_syncs_agents(self, tmp_path: Path) -> None:
        """Should sync agent files."""
        (tmp_path / "agents").mkdir()
        agent_file = tmp_path / "agents" / "test_agent.md"
        agent_file.write_text("""---
model: old-model
---
# Agent
""")

        config = {"metaModels": {"test_agent": {"model": "new-model", "thinking": "high"}}, "agents": {"test_agent": "test_agent"}}

        result = sync_new.sync_models(config, tmp_path)

        assert "test_agent" in result["agents"]
        assert len(result["errors"]) == 0

    def test_syncs_prompts(self, tmp_path: Path) -> None:
        """Should sync prompt files."""
        (tmp_path / "prompts").mkdir()
        prompt_file = tmp_path / "prompts" / "test_prompt.md"
        prompt_file.write_text("""---
model: old-model
---
# Prompt
""")

        config = {"metaModels": {"test_prompt": {"model": "new-model", "thinking": "low"}}, "prompts": {"test_prompt": "test_prompt"}}

        result = sync_new.sync_models(config, tmp_path)

        assert "test_prompt" in result["prompts"]
        assert len(result["errors"]) == 0

    def test_handles_errors_gracefully(self, tmp_path: Path) -> None:
        """Should handle errors gracefully."""
        (tmp_path / "agents").mkdir()
        agent_file = tmp_path / "agents" / "broken.md"
        agent_file.write_text("not valid frontmatter")

        config = {}

        # Should not raise
        result = sync_new.sync_models(config, tmp_path)
        # No errors because no frontmatter pattern matches
        assert len(result["errors"]) == 0


class TestResolveTargetBase:
    """Tests for resolve_target_base function."""

    def test_uses_project_arg(self, tmp_path: Path) -> None:
        """Should use project argument."""
        args = mock.Mock(project=str(tmp_path / "project"), global_install=False)
        result, ignore_project = sync_new.resolve_target_base(args)
        assert result == tmp_path / "project" / ".pi"
        assert ignore_project is False

    def test_uses_global_when_flag_set(self, tmp_path: Path) -> None:
        """Should use global path when --global flag set."""
        with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "home"):
            args = mock.Mock(project=None, global_install=True)
            result, ignore_project = sync_new.resolve_target_base(args)
            assert result == tmp_path / "home" / ".pi" / "agent"
            assert ignore_project is True

    def test_uses_cwd_pi_when_exists(self, tmp_path: Path) -> None:
        """Should use cwd/.pi when it exists."""
        (tmp_path / ".pi").mkdir()
        with mock.patch("tf_cli.sync_new.Path.cwd", return_value=tmp_path):
            args = mock.Mock(project=None, global_install=False)
            result, ignore_project = sync_new.resolve_target_base(args)
            assert result == tmp_path / ".pi"
            assert ignore_project is False

    def test_falls_back_to_global(self, tmp_path: Path) -> None:
        """Should fall back to global when no .pi in cwd."""
        with mock.patch("tf_cli.sync_new.Path.cwd", return_value=tmp_path):
            with mock.patch("tf_cli.sync_new.Path.home", return_value=tmp_path / "home"):
                args = mock.Mock(project=None, global_install=False)
                result, ignore_project = sync_new.resolve_target_base(args)
                assert result == tmp_path / "home" / ".pi" / "agent"
                assert ignore_project is True


class TestRunSync:
    """Tests for run_sync function."""

    def test_returns_success(self, tmp_path: Path) -> None:
        """Should return 0 on success."""
        (tmp_path / ".pi" / "agents").mkdir(parents=True)
        (tmp_path / ".pi" / "prompts").mkdir()

        args = mock.Mock(project=str(tmp_path), global_install=False)

        with mock.patch("tf_cli.sync_new.load_workflow_config", return_value={}):
            with mock.patch("tf_cli.sync_new.sync_models", return_value={"agents": [], "prompts": [], "errors": []}):
                result = sync_new.run_sync(args)
                assert result == 0

    def test_returns_error_on_sync_errors(self, tmp_path: Path) -> None:
        """Should return 1 on sync errors."""
        args = mock.Mock(project=str(tmp_path), global_install=False)

        with mock.patch("tf_cli.sync_new.load_workflow_config", return_value={}):
            with mock.patch("tf_cli.sync_new.sync_models", return_value={"agents": [], "prompts": [], "errors": ["error1"]}):
                result = sync_new.run_sync(args)
                assert result == 1


class TestMain:
    """Tests for main function."""

    def test_runs_sync_successfully(self) -> None:
        """Should run sync and return result."""
        with mock.patch("tf_cli.sync_new.run_sync", return_value=0) as mock_run:
            result = sync_new.main([])
            assert result == 0
            mock_run.assert_called_once()

    def test_parses_project_arg(self) -> None:
        """Should parse --project argument."""
        with mock.patch("tf_cli.sync_new.run_sync") as mock_run:
            sync_new.main(["--project", "/some/path"])
            args = mock_run.call_args[0][0]
            assert args.project == "/some/path"

    def test_parses_global_flag(self) -> None:
        """Should parse --global flag."""
        with mock.patch("tf_cli.sync_new.run_sync") as mock_run:
            sync_new.main(["--global"])
            args = mock_run.call_args[0][0]
            assert args.global_install is True
