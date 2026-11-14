"""Catalogue coverage without a Streamlit runtime dependency."""

from pathlib import Path

from dashboard_catalogue import CATEGORIES, TOOLS, TOOL_BY_SLUG, category_tools, search_tools


def test_registry_unique_and_sources_exist():
    assert len(TOOLS) == 34
    assert len(TOOL_BY_SLUG) == 34
    assert set(CATEGORIES) == {tool.category for tool in TOOLS}
    assert all(Path(tool.source).exists() for tool in TOOLS)


def test_search_by_category_and_terms():
    assert len(search_tools()) == 34
    assert "pdf-to-word" in {tool.slug for tool in search_tools("pdf docx")}
    assert "compress-image" in {tool.slug for tool in search_tools("jpeg")}
    assert search_tools("nonexistentstring") == ()
    assert all(tool.category == "File Handling" for tool in search_tools("pdf", "File Handling"))
    assert all(category_tools(category) for category in CATEGORIES)


def test_local_only_restrictions():
    for slug in ("disk-usage", "file-tree", "git-status", "hf-delete-folder", "github-repos"):
        assert TOOL_BY_SLUG[slug].local_only
    assert not TOOL_BY_SLUG["pdf-to-word"].local_only
