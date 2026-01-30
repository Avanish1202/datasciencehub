import streamlit as st
import pandas as pd
import datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURATION ---
ADMIN_USER = "avanish1202"
ADMIN_PASS = "1202"

# Google Sheets URL - embedded directly in code
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RY-l0IvjXf5AVecKv9uffOa8BCHWfY048WAmBdxVkD8/edit?usp=sharing"

# --- GOOGLE SHEETS CONNECTION ---
@st.cache_resource
def get_connection():
    """Create cached Google Sheets connection"""
    return st.connection("gsheets", type=GSheetsConnection)

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Data Science Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme in session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ... [ALL YOUR CSS STYLING CODE REMAINS THE SAME] ...
