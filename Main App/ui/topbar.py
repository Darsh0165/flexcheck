import streamlit as st

_HIDE_SIDEBAR = (
    "<style>[data-testid='stSidebar'],[data-testid='stSidebarCollapsedControl'],"
    "[data-testid='collapsedControl']{display:none !important}</style>"
)


def render_topbar():
    """Top navigation bar. Call this first on every page except Workout."""
    st.markdown(_HIDE_SIDEBAR, unsafe_allow_html=True)

    with st.container(key="topbar"):
        c = st.columns([1, 1, 1.9, 1, 4, 1.7], vertical_alignment="center")
        c[0].page_link("views/overview.py", label="Overview")
        c[1].page_link("views/history.py", label="History")
        c[2].page_link("views/schedule.py", label="Schedule & Analytics")
        c[3].page_link("views/about.py", label="About")

        with c[5].popover(f"👤 {st.session_state.get('username', 'User')}", width="stretch"):
            if st.button("Logout", key="logout_topbar", width="stretch"):
                st.session_state.clear()
                st.rerun()
