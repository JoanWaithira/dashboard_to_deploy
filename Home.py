import streamlit as st
import geopandas as gpd
import streamlit_folium
from folium import Map, GeoJson, FeatureGroup
from shapely.geometry import Point
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Zwolle Solar Dashboard", layout="wide", initial_sidebar_state="collapsed")
# --- Load local image and convert to base64 ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

img_base64 = get_base64_image("assets/solar.jpg")

# --- LOAD DISTRICTS ---
@st.cache_data
def load_districts():
    return gpd.read_file("assets/Wijkgrenzen_Zwolle.shp").to_crs(epsg=4326)

districts = load_districts()
district_name_column = "OMSCHR"

# --- CUSTOM CSS ---
# --- Custom Styling to Match Figma Header ---
# --- CUSTOM CSS to exactly match image design ---
st.markdown(f"""
    <style>
        .figma-header {{
            background-color: #c8bab2;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0;
            border-radius: 0px;
            margin: 0;
        }}
        .figma-header-left {{
            display: flex;
            align-items: center;
        }}
        .figma-solar-image {{
            width: 210px;
            height: 100%;
            object-fit: cover;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
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
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
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



# --- LAYOUT: Description | Map ---
col1, col2 = st.columns([1.25, 1])

# --- LEFT PANEL: Why Solar Dashboard ---
with col1:
    st.markdown("""
        <div class="info-card">
            <h3>Why a Solar Dashboard?</h3>
            <p>Transitioning to renewable energy is essential for sustainability.<br>
            Solar power offers Zwolle a key opportunity.</p>
            <p><strong>This dashboard helps by:</strong></p>
            <ul>
                <li> Assessing solar potential</li>
                <li> Simulating energy output for different adoption levels</li>
                <li> Evaluating Economics (Cost and Benefit)</li>
                <li>Tracking energy flow</li>
            </ul>
            <p><strong>How to Proceed:</strong><br>
            ➤ Select your district on the interactive map and explore its solar potential.</p>
        </div>
    """, unsafe_allow_html=True)

# --- RIGHT PANEL: Map + Selector ---
with col2:
    st.subheader("Select Your District")

    # Build interactive folium map
    m = Map(location=[52.516, 6.1], zoom_start=12)
    feature_group = FeatureGroup(name="Districts")

    for _, row in districts.iterrows():
        name = row[district_name_column]
        gj = GeoJson(
            data=row.geometry.__geo_interface__,
            name=name,
            tooltip=name,
            popup=name,
        )
        feature_group.add_child(gj)

    m.add_child(feature_group)

    map_output = streamlit_folium.st_folium(m, width=500, height=450)

    # Handle click event
    if map_output and "last_object_clicked" in map_output and map_output["last_object_clicked"]:
        lat, lon = map_output["last_object_clicked"]["lat"], map_output["last_object_clicked"]["lng"]
        clicked_point = Point(lon, lat)
        matched = districts[districts.contains(clicked_point)]

        if not matched.empty:
            selected_district = matched.iloc[0][district_name_column]
            st.session_state["selected_district"] = selected_district
            st.success(f"Selected district: **{selected_district}**")
        else:
            st.session_state["selected_district"] = None
            st.warning("No matching district found!")

    # Auto → Manual fallback
    if "selected_district" in st.session_state and st.session_state["selected_district"]:
        if st.button("Explore Solar Potential"):
            st.switch_page("pages/districts.py")

    selected = st.selectbox("Or pick a district manually:", districts[district_name_column].sort_values())
    if st.button("Explore Solar Potential (Manual)"):
        st.session_state["selected_district"] = selected
        st.switch_page("pages/districts.py")
