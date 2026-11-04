import streamlit as st

from services.auth.user_db import init_user_db, register_user, verify_user


def render_login_wall():
    if st.session_state.get("user_id") is not None:
        return True

    init_user_db()

    # Centre the form on wide screens; on phones the columns stack automatically
    _, mid, _ = st.columns([1, 2, 1])

    with mid:
        st.title("🦵 FlexCheck")
        st.markdown("### AI Workout Form Analyzer")

        tab_login, tab_register = st.tabs(["Login", "Register"])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", width="stretch")

            if submit:
                user = verify_user(username.strip(), password)
                if user is None:
                    st.error("Invalid username or password.")
                else:
                    st.session_state["user_id"] = user["id"]
                    st.session_state["username"] = user["username"]
                    st.rerun()

        with tab_register:
            with st.form("register_form"):
                r_user = st.text_input("Choose a username")
                r_email = st.text_input("Email")
                r_pass = st.text_input("Password", type="password")
                r_conf = st.text_input("Confirm password", type="password")
                r_submit = st.form_submit_button("Create account", width="stretch")

            if r_submit:
                ok, msg = register_user(r_user.strip(), r_email.strip(), r_pass, r_conf)
                (st.success if ok else st.error)(msg)

    return False
