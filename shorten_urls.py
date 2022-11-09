import hashlib
from typing import Optional
from urllib import parse

import streamlit as st

from db import insert_row, select_where

TABLE = "url_table"
DEFAULT_HASH_LENGTH = 6
BASE_URL = "https://playground.streamlitapp.com"


def get_hash(data: str, length: int = DEFAULT_HASH_LENGTH) -> str:
    """
    Given a string representation of data, return a length-characters-long string hash
    """
    return hashlib.md5(data.encode()).hexdigest()[:length]


def get_python() -> str:
    return st.session_state["python"]


def get_hash_from_python() -> str:
    return get_hash(get_python())


def get_python_from_hash(hash: str) -> str:
    row = select_where(TABLE, "python", "hash", hash)
    return row[0]["python"]


def is_hash_in_table(hash: str) -> bool:
    row = select_where(TABLE, "hash", "hash", hash)
    return len(row) > 0


def save_hash_if_not_exists(hash: Optional[str] = None) -> str:
    if hash is None:
        hash = get_hash_from_python()

    if not is_hash_in_table(hash):
        python = get_python()
        insert_row({"hash": hash, "python": python}, TABLE)
    return hash


def get_short_url_from_hash(hash: str) -> str:
    return BASE_URL + "?" + parse.urlencode({"q": hash})


def get_short_url_button():
    custom_hash = st.text_input("Custom Hash").strip()
    if st.button("Get shareable url"):
        if custom_hash:
            hash = custom_hash
        else:
            hash = get_hash_from_python()
        save_hash_if_not_exists(hash)
        url = get_short_url_from_hash(hash)
        st.write(url)


def expand_short_url():
    query_params = st.experimental_get_query_params()
    if "q" in query_params:
        short_hash = query_params["q"][0]
        try:
            python = get_python_from_hash(short_hash)
            st.session_state["python"] = python
        except IndexError:
            st.error(f"Invalid short url: {short_hash}")
