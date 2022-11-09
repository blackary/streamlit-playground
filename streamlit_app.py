import streamlit as st
from streamlit_ace import st_ace

from shorten_urls import expand_short_url, get_short_url_button

expand_short_url()

if "python" not in st.session_state:
    st.session_state["python"] = ""


def execute(code: str):
    try:
        exec(code, globals(), globals())
    except Exception as e:
        st.exception(e)


edit_pw = st.experimental_get_query_params().get("edit_password", [""])[0]

if edit_pw == st.secrets["edit_password"]:
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
