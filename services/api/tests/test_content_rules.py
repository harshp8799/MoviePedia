"""Unit tests for pure domain rules — no I/O."""

import pytest
from app.core.exceptions import ConflictError, ValidationError
from app.domain.services import content_rules
from app.domain.value_objects.enums import ContentType, Visibility


def test_slugify_basic():
    assert content_rules.slugify("The Long Winter!") == "the-long-winter"


def test_slugify_rejects_empty():
    with pytest.raises(ValidationError):
        content_rules.slugify("!!!")


def test_search_tokens_include_prefixes():
    tokens = content_rules.build_search_tokens("Neon", [])
    assert "n" in tokens and "ne" in tokens and "neon" in tokens


def test_valid_transitions():
    content_rules.validate_transition("draft", "published")
    content_rules.validate_transition("published", "archived")
    content_rules.validate_transition("archived", "published")


def test_same_state_transition_conflicts():
    with pytest.raises(ConflictError):
        content_rules.validate_transition("published", "published")


def test_assemble_content_doc_starts_as_draft():
    doc = content_rules.assemble_content_doc(
        ContentType.MOVIE, {"title": "Neon Horizon", "genres": ["sci-fi"]}, "actor1"
    )
    assert doc["type"] == "movie"
    assert doc["visibility"] == Visibility.DRAFT.value
    assert doc["slug"] == "neon-horizon"
    assert doc["createdBy"] == "actor1"
    assert "neon" in doc["searchTokens"]
