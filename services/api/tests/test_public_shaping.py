"""Unit tests for public response shaping — internal fields must never leak."""

from app.application.services.public_catalog_service import _child, _detail, _summary

_DOC = {
    "id": "x",
    "type": "movie",
    "slug": "s",
    "title": "T",
    "releaseYear": 2020,
    "genres": ["a"],
    "poster": {"url": "p"},
    "fullDescription": "F",
    "searchTokens": ["t"],
    "createdBy": "u",
    "updatedBy": "u",
    "visibility": "published",
    "schemaVersion": 1,
}

_INTERNAL = {"searchTokens", "createdBy", "updatedBy", "visibility", "schemaVersion"}


def test_summary_strips_internal_fields():
    out = _summary(_DOC)
    assert _INTERNAL.isdisjoint(out.keys())
    assert out["title"] == "T"
    assert out["poster"] == {"url": "p"}


def test_detail_includes_descriptions_but_no_internals():
    out = _detail(_DOC)
    assert out["fullDescription"] == "F"
    assert _INTERNAL.isdisjoint(out.keys())


def test_child_drops_timestamps():
    out = _child({"seasonNumber": 1, "title": "S1", "createdAt": "ts", "updatedAt": "ts"})
    assert "createdAt" not in out and "updatedAt" not in out
    assert out["seasonNumber"] == 1
