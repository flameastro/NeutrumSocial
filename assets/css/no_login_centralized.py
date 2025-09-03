import streamlit as st

def set_style(button: bool, text: bool, title: bool):
    if button:
        st.markdown('''
        <style>
            div[data-testid="stButton"] {
                text-align: center;
            }
        </style>
        ''', unsafe_allow_html=True)

    if text:
        st.markdown('''
        <style>
            div[data-testid="stCaptionContainer"] {
                text-align: center;
            }
        </style>
        ''', unsafe_allow_html=True)

    if title:
        st.markdown('''
        <style>
            h1 {
                text-align: center;
            }
        </style>
        ''', unsafe_allow_html=True)
