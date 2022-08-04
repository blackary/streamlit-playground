import streamlit as st
from streamlit_ace import st_ace

from shorten_urls import expand_short_url, get_short_url_button

expand_short_url()

if "python" not in st.session_state:
    st.session_state["python"] = ""


def execute(code: str):
    try:
        exec(code)
    except Exception as e:
        st.exception(e)

if st.experimental_user["email"] in st.secrets["authorized_users"]:
    python = st_ace(
        value=st.session_state["python"],
        key="python",
        language="python",
        min_lines=20,
    )
    get_short_url_button()

else:
    st.expander("Show code").code(st.session_state["python"])


execute(st.session_state["python"])
