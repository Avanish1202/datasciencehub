import streamlit as st
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
DATA_FILE = "resources.csv"
ADMIN_USER = "avanish1202"
ADMIN_PASS = "1202"

# --- PAGE SETUP ---
st.set_page_config(
    page_title="Data Science Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLING ---
st.markdown("""
<style>
    /* 1. HIDE DEFAULT ELEMENTS */
    [data-testid="stSidebar"] { display: none; } 
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stApp { background-color: #ffffff; }

    /* 2. HEADER & HERO (UPDATED COLORS) */
    .nav-logo {
        font-size: 24px; font-weight: 800; color: #1a1a1a; text-decoration: none;
    }
    .hero-box {
        text-align: center; 
        padding: 60px 20px;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        border-radius: 20px; 
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .hero-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        margin: 0;
        /* Main Title Gradient (Purple to Blue) */
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle { 
        font-size: 2.5rem; 
        font-weight: 700; 
        margin-top: 5px; 
        /* Subtitle Gradient (Matching the Title) */
        background: -webkit-linear-gradient(45deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc { 
        font-size: 1.15rem; 
        font-weight: 500;
        /* Descriptive Text Color (Deep Purple/Blue - Not Black) */
        color: #4c1d95; 
        margin-top: 20px; 
        max-width: 800px; 
        margin-left: auto; 
        margin-right: auto;
        line-height: 1.6;
    }
    .highlight {
        color: #2575fc;
        font-weight: 600;
    }

    /* 3. SUBJECT CARDS */
    .card-link { text-decoration: none !important; color: inherit; display: block; }
    .subject-card {
        padding: 30px; border-radius: 16px; height: 200px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        text-align: center; cursor: pointer;
        border: 1px solid rgba(0,0,0,0.04);
    }
    .subject-card:hover { transform: translateY(-5px); box-shadow: 0 10px 25px rgba(0,0,0,0.08); }
    .card-icon { font-size: 50px; margin-bottom: 15px; }
    .card-title { font-size: 1.5rem; font-weight: 700; color: #2d3748; }

    /* Card Colors */
    .bg-python { background-color: #fef9c3; } 
    .bg-mysql { background-color: #f1f5f9; }  
    .bg-powerbi { background-color: #fff7ed; } 
    .bg-ml { background-color: #fae8ff; }      
    .bg-stats { background-color: #dcfce7; }   
    .bg-other { background-color: #e0f2fe; }   

    /* 4. RESOURCE LIST */
    .resource-item {
        background: white; border: 1px solid #eee; border-radius: 12px;
        padding: 15px 20px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
        transition: box-shadow 0.2s;
    }
    .resource-item:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    .res-icon {
        width: 40px; height: 40px; background: #f3f0ff; color: #7c3aed;
        border-radius: 8px; display: flex; align-items: center; justify-content: center;
        font-size: 20px; margin-right: 15px;
    }
    .res-link-btn {
        background: #8b5cf6; color: white !important;
        text-decoration: none !important; padding: 8px 16px;
        border-radius: 6px; font-size: 0.9rem; font-weight: 500;
    }
    .res-link-btn:hover { opacity: 0.9; }

    /* 5. ADMIN UTILS */
    [data-testid="stPopover"] > button { border: none; background: transparent; color: #555; }
    [data-testid="stPopover"] > button:hover { color: #000; background: #f5f5f5; }
    a { text-decoration: none !important; }
</style>
""", unsafe_allow_html=True)
# --- DATA FUNCTIONS ---
def load_data():
    required_columns = ["Title", "Category", "Link", "Date_Added"]
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=required_columns)
        df.to_csv(DATA_FILE, index=False)
        return df
    
    df = pd.read_csv(DATA_FILE)
    # Fix missing columns if file is old
    save_required = False
    for col in required_columns:
        if col not in df.columns:
            df[col] = datetime.date.today()
            save_required = True
    if save_required:
        df.to_csv(DATA_FILE, index=False)
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- NAVIGATION ---
query_params = st.query_params
current_page = query_params.get("page", "Home")

# --- HEADER (Logo + Login) ---
col_logo, col_admin = st.columns([10, 1])
with col_logo:
    st.markdown('<a href="?page=Home" class="nav-logo">DataSci Hub</a>', unsafe_allow_html=True)

with col_admin:
    # Top Right Login Popup
    with st.popover("👤", help="Admin Access"):
        st.markdown("### Admin Login")
        if "is_admin" not in st.session_state:
            st.session_state.is_admin = False
            
        if not st.session_state.is_admin:
            with st.form("login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if u == ADMIN_USER and p == ADMIN_PASS:
                        st.session_state.is_admin = True
                        st.rerun()
                    else:
                        st.error("Invalid")
        else:
            st.success("Logged In")
            if st.button("Logout"):
                st.session_state.is_admin = False
                st.rerun()

# --- MAIN CONTENT ---

if current_page == "Home":
    # Hero
    st.markdown("""
        <div class="hero-box">
            <h1 class="hero-title">Master Data Science</h1>
            <h1 class="hero-subtitle">One Resource at a Time</h1>
            <p class="hero-text">Select a topic below to access curated notes, videos, and datasets.</p>
        </div>
    """, unsafe_allow_html=True)

    # Cards
    st.markdown("### 📚 Explore Subjects")
    def card(title, icon, color_class):
        return f"""
        <a href="?page={title}" class="card-link" target="_self">
            <div class="subject-card {color_class}">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
            </div>
        </a>
        """
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(card("Python", "🐍", "bg-python"), unsafe_allow_html=True)
    with c2: st.markdown(card("MySQL", "🗄️", "bg-mysql"), unsafe_allow_html=True)
    with c3: st.markdown(card("Power BI", "📊", "bg-powerbi"), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c4, c5, c6 = st.columns(3)
    with c4: st.markdown(card("Machine Learning", "🤖", "bg-ml"), unsafe_allow_html=True)
    with c5: st.markdown(card("Descriptive Statistics", "📈", "bg-stats"), unsafe_allow_html=True)
    with c6: st.markdown(card("Other", "📁", "bg-other"), unsafe_allow_html=True)

else:
    # --- SUBJECT PAGE ---
    
    # 1. Page Header
    gradients = {
        "Python": "linear-gradient(90deg, #fce38a 0%, #f38181 100%)",
        "MySQL": "linear-gradient(90deg, #a1c4fd 0%, #c2e9fb 100%)",
        "Power BI": "linear-gradient(90deg, #fbc2eb 0%, #a6c1ee 100%)",
        "Machine Learning": "linear-gradient(90deg, #fad0c4 0%, #ffd1ff 100%)",
        "Descriptive Statistics": "linear-gradient(90deg, #d4fc79 0%, #96e6a1 100%)",
        "Other": "linear-gradient(90deg, #e6e9f0 0%, #eef1f5 100%)"
    }
    bg = gradients.get(current_page, "#eee")
    
    st.markdown(f"""
        <div style="background:{bg}; padding:40px; border-radius:15px; text-align:center; color:white; margin-bottom:20px;">
            <h1 style="margin:0; font-size:3rem; text-shadow:0 1px 3px rgba(0,0,0,0.1);">{current_page}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. ADMIN ADD SECTION (MOVED TO TOP)
    if st.session_state.get("is_admin"):
        with st.expander(f"➕ Add New {current_page} Resource", expanded=False):
            with st.form("add_res_top"):
                c_add1, c_add2 = st.columns([1, 2])
                t = c_add1.text_input("Title")
                l = c_add2.text_input("Drive Link")
                if st.form_submit_button("Upload Resource"):
                    if t and l:
                        df_load = load_data()
                        new_row = pd.DataFrame([[t, current_page, l, datetime.date.today()]], 
                                             columns=["Title", "Category", "Link", "Date_Added"])
                        df_load = pd.concat([df_load, new_row], ignore_index=True)
                        save_data(df_load)
                        st.success("Added!")
                        st.rerun()

    # 3. Nav & Search
    col_nav, col_search = st.columns([1, 4])
    with col_nav:
        st.markdown('<a href="?page=Home" target="_self" style="text-decoration:none !important; display:inline-block; padding:8px 15px; background:#f0f2f6; color:#333; border-radius:5px; font-weight:500;">← Back Home</a>', unsafe_allow_html=True)
    with col_search:
        search_q = st.text_input("Search", placeholder="Find resources...", label_visibility="collapsed")

    # 4. List Resources
    df = load_data()
    filtered = df[df['Category'] == current_page]
    if search_q:
        filtered = filtered[filtered['Title'].str.contains(search_q, case=False, na=False)]

    st.write("") 
    if filtered.empty:
        st.info(f"No content in {current_page} yet.")
    else:
        for idx, row in filtered.iterrows():
            date_val = row.get('Date_Added', 'N/A')
            
            st.markdown(f"""
            <div class="resource-item">
                <div style="display:flex; align-items:center;">
                    <div class="res-icon">📄</div>
                    <div>
                        <div style="font-weight:bold; color:#333;">{row['Title']}</div>
                        <div style="font-size:0.8rem; color:#888;">{date_val}</div>
                    </div>
                </div>
                <a href="{row['Link']}" target="_blank" class="res-link-btn">View</a>
            </div>
            """, unsafe_allow_html=True)
            
            # Admin Delete Button
            if st.session_state.get("is_admin"):
                if st.button("🗑️ Delete", key=f"del_{idx}"):
                    df = df.drop(idx)
                    save_data(df)
                    st.rerun()


