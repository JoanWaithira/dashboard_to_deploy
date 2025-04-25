
import streamlit as st
import streamlit.components.v1 as components
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Zwolle Solar Simulation Dashboard", layout="wide")

# --- Load header image ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("assets/solar.jpg")

# --- HEADER ---
st.markdown(f"""
    <style>
        .figma-header {{
            background-color: #c8bab2;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0;
            margin-bottom: 2rem;
        }}
        .figma-header-left {{
            display: flex;
            align-items: center;
        }}
        .figma-solar-image {{
            width: 210px;
            height: 100%;
            object-fit: cover;
        }}
        .figma-title-block {{
            padding: 20px 40px;
            text-align: center;
            flex-grow: 1;
        }}
        .figma-title {{
            font-size: 24px;
            font-weight: bold;
            color: black;
            margin-bottom: 6px;
            font-family: Georgia, serif;
        }}
        .figma-subtitle {{
            font-size: 15px;
            font-style: italic;
            color: black;
        }}
        .figma-zwolle {{
            background-color: #3a65a8;
            color: white;
            padding: 15px 30px;
            font-weight: bold;
            font-size: 20px;
            font-family: Georgia, serif;
        }}

        /* Panel Styling */
        .panel {{
            background-color: #ececec;
            padding: 30px;
            border-radius: 25px;
            font-family: Georgia, serif;
        }}

        /* Yellow buttons */
        .yellow-btn > button {{
            background-color: #ffdd57;
            color: black;
            font-weight: bold;
            border-radius: 30px;
            padding: 12px 24px;
            font-size: 16px;
            font-family: Georgia, serif;
            border: none;
        }}

        .yellow-btn > button:hover {{
            background-color: #f7cd45;
            transform: scale(1.01);
        }}

        .stRadio > div, .stMultiSelect > div {{
            background-color: transparent;
        }}
    </style>

    <div class="figma-header">
        <div class="figma-header-left">
            <img class="figma-solar-image" src="data:image/jpeg;base64,{img_base64}" alt="Solar Panel">
        </div>
        <div class="figma-title-block">
            <div class="figma-title">WELCOME TO THE ZWOLLE SOLAR DASHBOARD</div>
            <div class="figma-subtitle">Track, Simulate & Optimize Solar Energy in Your District</div>
        </div>
        <div class="figma-zwolle">Zwolle</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("## Scenario Outcome: Industry – Level 2 Suitability (100% Adoption)")

# --- First Row ---
col1, col2 = st.columns(2)
with col1:
    components.html(open("fig1_production.html", 'r').read(), height=360, scrolling=False)
with col2:
    components.html(open("fig2_storage.html", 'r').read(), height=360, scrolling=False)

# --- Second Row ---
col3, col4 = st.columns(2)
with col3:
    components.html(open("fig3_panels.html", 'r').read(), height=300, scrolling=False)
with col4:
    components.html(open("fig_payback_only.html", 'r').read(), height=360, scrolling=False)

# --- Third Row ---
components.html(open("fig_investment_only.html", 'r').read(), height=360, scrolling=False)

# --- Action Buttons ---
st.markdown("### ")
col_btn1, col_btn2 = st.columns([1, 1])
with col_btn1:
    if st.button("⬅ CHOOSE ANOTHER SCENARIO"):
        st.switch_page("pages/2_ScenarioSelection.py")
with col_btn2:
    if st.button("📥 DOWNLOAD THE RESULTS"):
        st.success("Results will download soon...")
