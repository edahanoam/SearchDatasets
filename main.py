import streamlit as st
import pandas as pd


def page_set():
    st.set_page_config(page_title="Dataset Search", page_icon="🐍", layout="wide")
    st.title("Summarization Datasets Search Engine")


def connect_to_doc(local=False):
    if not local:
        # Connect to the Google Sheet
        url = "https://docs.google.com/spreadsheets/d/1uJqKosaAD0paPTJHT7-g0Ssw_P-X1Mp7aOchFFKGN4M/edit?usp=sharing"
        df = pd.read_csv(url, dtype=str).fillna("")
        st.write(df)
    else:
        df = pd.read_csv("after_unifying.csv", dtype=str).fillna("")
        st.write(df)





if __name__ == '__main__':
    page_set()
    connect_to_doc(True)




