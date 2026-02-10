"""Tests for tf.utils module."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tf.utils import (
    DEFAULT_TIMEOUT_INCREMENT_MS,
    calculate_timeout_backoff,
    find_project_root,
    merge,
    read_json,
)


class TestReadJson:
    """Tests for read_json function."""

    def test_reads_valid_json(self, tmp_path: Path) -> None:
        """Test reading a valid JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "nested": {"a": 1}}
        test_file.write_text(json.dumps(test_data))

        result = read_json(test_file)
        assert result == test_data

    def test_returns_empty_dict_for_missing_file(self, tmp_path: Path) -> None:
        """Test that missing file returns empty dict."""
        missing_file = tmp_path / "nonexistent.json"

        result = read_json(missing_file)
        assert result == {}

    def test_returns_empty_dict_for_invalid_json(self, tmp_path: Path) -> None:
        """Test that invalid JSON returns empty dict."""
        test_file = tmp_path / "invalid.json"
        test_file.write_text("not valid json")

        result = read_json(test_file)
        assert result == {}

    def test_handles_unicode_content(self, tmp_path: Path) -> None:
        """Test reading JSON with unicode content."""
        test_file = tmp_path / "unicode.json"
        test_data = {"message": "Hello, 世界! 🌍"}
        test_file.write_text(json.dumps(test_data, ensure_ascii=False), encoding="utf-8")

        result = read_json(test_file)
        assert result == test_data


class TestFindProjectRoot:
    """Tests for find_project_root function."""

    def test_finds_tf_directory(self, tmp_path: Path) -> None:
        """Test finding project root with .tf directory."""
        # Create .tf directory
        tf_dir = tmp_path / ".tf"
        tf_dir.mkdir()
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        result = find_project_root(subdir)
        assert result == tmp_path

    def test_finds_pi_directory(self, tmp_path: Path) -> None:
        """Test finding project root with .pi directory."""
        # Create .pi directory
        pi_dir = tmp_path / ".pi"
        pi_dir.mkdir()
        subdir = tmp_path / "subdir" / "nested"
        subdir.mkdir(parents=True)

        result = find_project_root(subdir)
        assert result == tmp_path

    def test_prefers_tf_over_parent_search(self, tmp_path: Path) -> None:
        """Test that .tf is found before searching parents."""
        # Create nested structure with .tf at both levels
        outer_tf = tmp_path / ".tf"
        outer_tf.mkdir()
        inner_dir = tmp_path / "inner"
        inner_dir.mkdir()
        inner_tf = inner_dir / ".tf"
        inner_tf.mkdir()

        result = find_project_root(inner_dir)
        # Should find the inner .tf first
        assert result == inner_dir

    def test_returns_none_when_no_marker(self, tmp_path: Path) -> None:
        """Test that None is returned when no marker directory exists."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()

        result = find_project_root(subdir)
        assert result is None

    def test_uses_cwd_when_no_start_given(self, tmp_path: Path, monkeypatch) -> None:
        """Test that current working directory is used when no start given."""
        tf_dir = tmp_path / ".tf"
        tf_dir.mkdir()
        monkeypatch.chdir(tmp_path)

        result = find_project_root()
        assert result == tmp_path

    def test_searches_parents(self, tmp_path: Path) -> None:
        """Test that function searches parent directories."""
        # Create nested structure
        tf_dir = tmp_path / ".tf"
        tf_dir.mkdir()
        level1 = tmp_path / "level1"
        level1.mkdir()
        level2 = level1 / "level2"
        level2.mkdir()
        level3 = level2 / "level3"
        level3.mkdir()

        result = find_project_root(level3)
        assert result == tmp_path


class TestMerge:
    """Tests for merge function."""

    def test_simple_merge(self) -> None:
        """Test merging two simple dicts."""
        a = {"x": 1, "y": 2}
        b = {"y": 3, "z": 4}

        result = merge(a, b)

        assert result == {"x": 1, "y": 3, "z": 4}

    def test_nested_merge(self) -> None:
        """Test merging nested dictionaries."""
        a = {"outer": {"inner1": "a", "inner2": "b"}}
        b = {"outer": {"inner2": "c", "inner3": "d"}}

        result = merge(a, b)

        assert result == {"outer": {"inner1": "a", "inner2": "c", "inner3": "d"}}

    def test_does_not_mutate_input(self) -> None:
        """Test that original dicts are not modified."""
        a = {"x": 1, "nested": {"a": 1}}
        b = {"y": 2, "nested": {"b": 2}}
        a_copy = {"x": 1, "nested": {"a": 1}}
        b_copy = {"y": 2, "nested": {"b": 2}}

        merge(a, b)

        assert a == a_copy
        assert b == b_copy

    def test_empty_dict_merge(self) -> None:
        """Test merging with empty dicts."""
        a = {"key": "value"}
        b = {}

        result = merge(a, b)
        assert result == {"key": "value"}

        result = merge(b, a)
        assert result == {"key": "value"}

    def test_deeply_nested_merge(self) -> None:
        """Test merging deeply nested structures."""
        a = {"level1": {"level2": {"level3": {"a": 1, "b": 2}}}}
        b = {"level1": {"level2": {"level3": {"b": 3, "c": 4}}}}

        result = merge(a, b)

        assert result == {"level1": {"level2": {"level3": {"a": 1, "b": 3, "c": 4}}}}

    def test_overwrites_non_dict_values(self) -> None:
        """Test that non-dict values are overwritten."""
        a = {"key": "string"}
        b = {"key": {"nested": "dict"}}

        result = merge(a, b)

        assert result == {"key": {"nested": "dict"}}

    def test_real_world_config_merge(self) -> None:
        """Test merging realistic config structures."""
        global_config = {
            "metaModels": {
                "worker": {"model": "gpt-4", "thinking": "high"}
            },
            "checkers": {
                "python": {"lint": "ruff", "format": "black"}
            }
        }
        project_config = {
            "metaModels": {
                "worker": {"model": "gpt-5"}  # Override model
            },
            "agents": {"reviewer": "worker"}  # New key
        }

        result = merge(global_config, project_config)

        expected = {
            "metaModels": {
                "worker": {"model": "gpt-5", "thinking": "high"}
            },
            "checkers": {
                "python": {"lint": "ruff", "format": "black"}
            },
            "agents": {"reviewer": "worker"}
        }
        assert result == expected


class TestCalculateTimeoutBackoff:
    """Tests for calculate_timeout_backoff function.

    Covers the linear timeout backoff computation:
    - effective = base_ms + iteration_index * increment_ms
    - Optional cap at max_ms
    """

    # === Iteration Index Semantics ===

    def test_iteration_index_zero_returns_base(self) -> None:
        """Test that iteration_index=0 returns base timeout (no increment added)."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=0,
        )
        assert result == 60000

    def test_iteration_index_one_adds_single_increment(self) -> None:
        """Test that iteration_index=1 adds exactly one increment to base."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=1,
        )
        assert result == 60000 + DEFAULT_TIMEOUT_INCREMENT_MS  # 210000

    def test_iteration_index_two_adds_two_increments(self) -> None:
        """Test that iteration_index=2 adds two increments to base."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=2,
        )
        assert result == 60000 + 2 * DEFAULT_TIMEOUT_INCREMENT_MS  # 360000

    # === Cap Behavior (max_timeout_ms) ===

    def test_cap_applied_when_effective_exceeds_max(self) -> None:
        """Test that max_ms cap is applied when effective exceeds it."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=2,
            max_ms=300000,
        )
        # Without cap: 60000 + 2*150000 = 360000
        # With cap: min(360000, 300000) = 300000
        assert result == 300000

    def test_cap_not_applied_when_effective_below_max(self) -> None:
        """Test that max_ms cap does not affect values under it."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=1,
            max_ms=300000,
        )
        # effective = 210000, under cap of 300000
        assert result == 210000

    def test_cap_exactly_at_max(self) -> None:
        """Test edge case where effective exactly equals max_ms."""
        result = calculate_timeout_backoff(
            base_ms=100000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=1,
            max_ms=250000,  # Exactly equals effective
        )
        assert result == 250000

    def test_cap_with_max_equal_to_base(self) -> None:
        """Test that max_ms == base_ms always returns base (full cap)."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
            iteration_index=5,
            max_ms=60000,
        )
        assert result == 60000  # Always capped at base

    def test_no_cap_when_max_ms_is_none(self) -> None:
        """Test that no cap is applied when max_ms is None."""
        result = calculate_timeout_backoff(
            base_ms=10000,
            increment_ms=10000,
            iteration_index=100,
            max_ms=None,
        )
        # Would be 10000 + 100*10000 = 1010000 without cap
        assert result == 1010000

    # === Non-Default Increment Override ===

    def test_non_default_increment_override(self) -> None:
        """Test using a custom increment value different from default."""
        result = calculate_timeout_backoff(
            base_ms=10000,
            increment_ms=5000,  # Custom increment
            iteration_index=3,
        )
        # effective = 10000 + 3*5000 = 25000
        assert result == 25000

    def test_zero_increment_constant_timeout(self) -> None:
        """Test with zero increment (constant timeout regardless of iteration)."""
        result = calculate_timeout_backoff(
            base_ms=60000,
            increment_ms=0,
            iteration_index=5,
        )
        assert result == 60000  # Always base, regardless of iteration

    def test_large_iteration_index(self) -> None:
        """Test behavior with large iteration index."""
        result = calculate_timeout_backoff(
            base_ms=10000,
            increment_ms=5000,
            iteration_index=100,
        )
        assert result == 10000 + 100 * 5000  # 510000

    # === Input Validation ===

    def test_zero_base_timeout_is_valid(self) -> None:
        """Test with zero base timeout."""
        result = calculate_timeout_backoff(
            base_ms=0,
            increment_ms=5000,
            iteration_index=5,
        )
        assert result == 25000

    def test_negative_base_ms_raises(self) -> None:
        """Test that negative base_ms raises ValueError."""
        with pytest.raises(ValueError, match="base_ms must be non-negative"):
            calculate_timeout_backoff(
                base_ms=-1000,
                increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
                iteration_index=0,
            )

    def test_negative_increment_ms_raises(self) -> None:
        """Test that negative increment_ms raises ValueError."""
        with pytest.raises(ValueError, match="increment_ms must be non-negative"):
            calculate_timeout_backoff(
                base_ms=60000,
                increment_ms=-1000,
                iteration_index=0,
            )

    def test_negative_iteration_index_raises(self) -> None:
        """Test that negative iteration_index raises ValueError."""
        with pytest.raises(ValueError, match="iteration_index must be non-negative"):
            calculate_timeout_backoff(
                base_ms=60000,
                increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
                iteration_index=-1,
            )

    def test_max_ms_less_than_base_raises(self) -> None:
        """Test that max_ms < base_ms raises ValueError."""
        with pytest.raises(ValueError, match="max_ms.*must be >= base_ms"):
            calculate_timeout_backoff(
                base_ms=60000,
                increment_ms=DEFAULT_TIMEOUT_INCREMENT_MS,
                iteration_index=0,
                max_ms=30000,  # Less than base_ms
            )

    def test_default_increment_constant_value(self) -> None:
        """Test that DEFAULT_TIMEOUT_INCREMENT_MS is 150000 ms."""
        assert DEFAULT_TIMEOUT_INCREMENT_MS == 150000
