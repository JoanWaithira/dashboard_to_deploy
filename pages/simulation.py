import streamlit as st
import geopandas as gpd
from folium import Map, GeoJson
from shapely.geometry import mapping
import streamlit_folium
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Select Scenario", layout="wide", initial_sidebar_state="collapsed")

# --- Load district from session ---
district = st.session_state.get("selected_district", None)

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

# --- LAYOUT ---
left_col, right_col = st.columns([1.2, 1])

# --- LEFT PANEL: Scenarios ---
with left_col:
    st.markdown("## Select your desired scenario")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <style>
            .stButton > button {
                background-color: #f4bcbc;
                border: none;
                border-radius: 12px;
                padding: 18px 15px;
                font-size: 16px;
                font-weight: bold;
                font-family: Georgia, serif;
                text-align: center;
                width: 100%;
                line-height: 1.4;
                transition: 0.2s ease;
                color: black;
            }

            .stButton > button:hover {
                background-color: #c8bab2;
                transform: scale(1.02);
                cursor: pointer;
            }
        </style>
    """, unsafe_allow_html=True)

    # Scenario buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Scenario One:\nIndustrial - Land Use"):
            st.session_state["scenario"] = "Industrial"
            st.switch_page("pages/choices.py")

    with col2:
        if st.button("Scenario Two:\nResidential - Land Use"):
            st.session_state["scenario"] = "Residential"
            st.switch_page("pages/choices.py")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("Scenario Three:\nOther - Land Use"):
            st.session_state["scenario"] = "Other"
            st.switch_page("pages/choices.py")
    with col4:
        if st.button("Scenario Four:\nAll Land Use Types"):
            st.session_state["scenario"] = "All"
            st.switch_page("pages/choices.py")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Scenario Five:\nSolar on Large Roofs"):
        st.session_state["scenario"] = "Large Roofs"
        st.switch_page("pages/choices.py")

# --- RIGHT PANEL: Map ---
with right_col:
    st.markdown("### District Map")

    @st.cache_data
    def load_districts():
        return gpd.read_file("assets/Wijkgrenzen_Zwolle.shp").to_crs(epsg=4326)

    if district:
        districts = load_districts()
        sel_geom = districts[districts["OMSCHR"] == district]
        centroid = sel_geom.geometry.centroid.iloc[0]
        fmap = Map(location=[centroid.y, centroid.x], zoom_start=13)
        geojson = GeoJson(data=mapping(sel_geom.geometry.iloc[0]), name=district, tooltip=district)
        geojson.add_to(fmap)
        streamlit_folium.st_folium(fmap, width=500, height=500)
    else:
        st.warning("No district selected.")
