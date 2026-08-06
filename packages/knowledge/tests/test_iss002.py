"""ISS-002 Tests: ID system hardening."""

import pytest
from athena_core.identity import is_valid_id, parse_id, generate_id


class TestISS002IsValidId:
    """ISS-002: is_valid_id edge cases."""

    def test_empty_string(self):
        assert is_valid_id("", "ent") is False

    def test_no_underscore(self):
        assert is_valid_id("entabc123", "ent") is False

    def test_wrong_prefix(self):
        assert is_valid_id("art_abc12345", "ent") is False

    def test_short_uuid(self):
        assert is_valid_id("ent_abc", "ent") is False

    def test_valid(self):
        assert is_valid_id("ent_abcdef12", "ent") is True

    def test_none_value(self):
        assert is_valid_id(None, "ent") is False  # type: ignore


class TestISS002ParseId:
    """ISS-002: parse_id function."""

    def test_parse_valid(self):
        prefix, uuid_part = parse_id("ent_a1b2c3d4")
        assert prefix == "ent"
        assert uuid_part == "a1b2c3d4"

    def test_parse_empty_raises(self):
        with pytest.raises(ValueError):
            parse_id("")

    def test_parse_no_underscore_raises(self):
        with pytest.raises(ValueError):
            parse_id("entabc123")

    def test_parse_short_uuid_raises(self):
        with pytest.raises(ValueError):
            parse_id("ent_abc")

    def test_parse_roundtrip(self):
        original = generate_id("src")
        prefix, uuid_part = parse_id(original)
        assert prefix == "src"
        assert len(uuid_part) >= 6
