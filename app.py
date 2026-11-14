"""Utility Shelf Dashboard v2.

The UI uses Streamlit only for navigation and widgets. Individual Python
snippets remain framework-independent in their original packages.
"""

from pathlib import Path
from urllib.parse import quote

import streamlit as st

from dashboard_catalogue import CATEGORIES, TOOLS, TOOL_BY_SLUG, category_tools, search_tools
from dashboard_handlers import LOCAL_TOOLS_ENABLED, TOOL_RENDERERS
from dashboard_style import stylesheet


def _picker_key(category: str) -> str:
    return "shelf_picker_" + "".join(c if c.isalnum() else "_" for c in category)


def _record_recent(slug: str) -> None:
    previous = list(st.session_state.get("shelf_recent", []))
    st.session_state["shelf_recent"] = [slug] + [s for s in previous if s != slug][:7]


def _open_tool(slug: str) -> None:
    tool = TOOL_BY_SLUG[slug]
    st.session_state["shelf_category"] = tool.category
    st.session_state[_picker_key(tool.category)] = slug
    st.session_state["shelf_active_tool"] = slug
    _record_recent(slug)


def _go_home() -> None:
    st.session_state["shelf_category"] = "Overview"


def _category_changed() -> None:
    category = st.session_state["shelf_category"]
    if category != "Overview":
        slug = st.session_state.get(_picker_key(category), category_tools(category)[0].slug)
        st.session_state["shelf_active_tool"] = slug


def _tool_changed() -> None:
    category = st.session_state["shelf_category"]
    slug = st.session_state[_picker_key(category)]
    st.session_state["shelf_active_tool"] = slug
    _record_recent(slug)


def _toggle_favourite(slug: str) -> None:
    favourites = list(st.session_state.get("shelf_favourites", []))
    if slug in favourites:
        favourites.remove(slug)
    else:
        favourites.append(slug)
    st.session_state["shelf_favourites"] = favourites


def _clear_results(slug: str) -> None:
    st.session_state.get("shelf_outputs", {}).pop(slug, None)
    st.session_state.get("shelf_values", {}).pop(slug, None)


def _display_results(slug: str) -> None:
    downloads = st.session_state.get("shelf_outputs", {}).get(slug, {})
    value = st.session_state.get("shelf_values", {}).get(slug)
    if not downloads and value is None:
        return
    st.divider()
    st.markdown("#### Your result")
    st.caption("Saved for this session. You can switch tools and return to download.")
    if value is not None:
        st.write(value)
    for index, output in enumerate(downloads.values()):
        if output["file_name"].lower().endswith(".wav"):
            st.audio(output["data"], format="audio/wav")
        st.download_button(
            output["label"],
            output["data"],
            file_name=output["file_name"],
            mime=output["mime"],
            key=f"result_{slug}_{index}",
            on_click="ignore",
            use_container_width=True,
        )
    st.button("Clear result", key=f"clear_{slug}",
              on_click=_clear_results, args=(slug,))


def _tool_tile(tool, context: str) -> None:
    with st.container(border=True):
        st.markdown(
            f'<div class="shelf-card-icon">{tool.icon}</div>'
            f'<div class="shelf-card-title">{tool.title}</div>'
            f'<div class="shelf-card-desc">{tool.description}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<span class="shelf-small">{"LOCAL ONLY" if tool.local_only else "INTERACTIVE"}</span>',
            unsafe_allow_html=True,
        )
        st.button("Open tool", key=f"open_{context}_{tool.slug}",
                  on_click=_open_tool, args=(tool.slug,),
                  use_container_width=True)


def _tile_grid(tools, context: str) -> None:
    if not tools:
        st.markdown(
            '<div class="shelf-empty">No matching tools. Try a different search or category.</div>',
            unsafe_allow_html=True,
        )
        return
    for offset in range(0, len(tools), 3):
        columns = st.columns(3, gap="medium")
        for column, tool in zip(columns, tools[offset:offset + 3]):
            with column:
                _tool_tile(tool, context)


def _overview() -> None:
    st.markdown(
        '<div class="shelf-hero"><span class="shelf-kicker">UTILITY SHELF / V2</span>'
        '<h1>Useful tools.<br>Less busywork.</h1>'
        '<p>A thoughtful collection of practical Python utilities for files, '
        'images, audio, text and developer workflows. Find a tool, get the job done, '
        'and take the underlying code with you.</p></div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Available tools", len(TOOLS))
    col2.metric("Categories", len(CATEGORIES))
    col3.metric("Browser-ready", sum(not tool.local_only for tool in TOOLS))
    st.markdown('<div class="shelf-section">Find a tool</div>', unsafe_allow_html=True)
    query = st.text_input(
        "Search tools", placeholder="Try PDF, images, Git, regex or audio",
        key="shelf_search",
    )
    category = st.selectbox("Category", ("All categories", *CATEGORIES), key="shelf_filter")
    scoped = None if category == "All categories" else category
    matches = search_tools(query, scoped)
    favs = set(st.session_state.get("shelf_favourites", []))
    recent = st.session_state.get("shelf_recent", ())
    tab_all, tab_favourites, tab_recent = st.tabs(
        ("Browse tools", "Favourites", "Recently used")
    )
    with tab_all:
        st.caption(f"{len(matches)} tools match your search.")
        _tile_grid(matches, "all")
    with tab_favourites:
        _tile_grid(tuple(tool for tool in matches if tool.slug in favs), "favourites")
    with tab_recent:
        by_slug = {tool.slug: tool for tool in matches}
        _tile_grid(tuple(by_slug[slug] for slug in recent if slug in by_slug), "recent")


def _workspace(category: str) -> None:
    items = category_tools(category)
    picker = _picker_key(category)
    if st.session_state.get(picker) not in {tool.slug for tool in items}:
        st.session_state[picker] = items[0].slug
    st.button("← Back to catalogue", key="back_home", on_click=_go_home)
    st.markdown(f'<span class="shelf-kicker">{category}</span>', unsafe_allow_html=True)
    slug = st.selectbox(
        "Select a tool",
        tuple(tool.slug for tool in items),
        format_func=lambda value: TOOL_BY_SLUG[value].title,
        key=picker,
        on_change=_tool_changed,
    )
    tool = TOOL_BY_SLUG[slug]
    st.session_state["shelf_active_tool"] = slug
    st.title(f"{tool.icon}  {tool.title}")
    st.caption(tool.description)
    left, right = st.columns([1, 3], vertical_alignment="center")
    with left:
        saved = slug in st.session_state.get("shelf_favourites", [])
        st.button(
            "★ Saved" if saved else "☆ Favourite",
            key=f"save_{slug}", on_click=_toggle_favourite, args=(slug,),
            use_container_width=True,
        )
    with right:
        st.caption("🔒 Local-only operation" if tool.local_only
                   else "✓ Available in the browser")
    tab_work, tab_code, tab_help = st.tabs(("Workspace", "Python snippet", "About"))
    with tab_work:
        if tool.local_only and not LOCAL_TOOLS_ENABLED:
            st.info(
                "This operation is disabled on the public server. "
                "Run locally with ENABLE_LOCAL_OPERATIONS=1."
            )
        with st.container(border=True):
            TOOL_RENDERERS[slug]()
        _display_results(slug)
    with tab_code:
        st.markdown(f'<div class="shelf-file">{tool.source}</div>',
                    unsafe_allow_html=True)
        file = Path(tool.source)
        if file.is_file():
            st.code(
                file.read_text(encoding="utf-8"),
                language="markdown" if file.suffix == ".md" else "python",
                line_numbers=True,
            )
        else:
            st.warning("The source file is unavailable in this environment.")
        st.link_button(
            "View source on GitHub",
            "https://github.com/AdityaSreevatsaK/Useful-Code-Snippets/blob/main/"
            + quote(tool.source, safe="/"),
        )
    with tab_help:
        st.markdown(f"### {tool.title}")
        st.write(tool.description)
        st.markdown(
            "This tool is backed by a standalone Python snippet. "
            "Open the **Python snippet** tab to inspect or copy its implementation."
        )
        if tool.local_only:
            st.warning("This tool must only run on a trusted local instance.")
        else:
            st.info(
                "Provide your input, run the operation, then download the generated "
                "result. Generated files are kept within your current browser session."
            )


st.set_page_config(
    page_title="Utility Shelf | Python Tools",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.sidebar.markdown("## ◈ Utility Shelf")
st.sidebar.caption("A curated Python toolbox")
st.sidebar.selectbox("Appearance", ("Light", "Dark"), key="shelf_appearance")
st.markdown(stylesheet(st.session_state["shelf_appearance"]), unsafe_allow_html=True)
selection = st.sidebar.radio(
    "Explore", ("Overview", *CATEGORIES), key="shelf_category",
    on_change=_category_changed,
)
st.sidebar.divider()
st.sidebar.caption(f"{len(TOOLS)} tools · {len(CATEGORIES)} collections")
st.sidebar.caption("Privileged utilities are local-only.")

if selection == "Overview":
    _overview()
else:
    _workspace(selection)
