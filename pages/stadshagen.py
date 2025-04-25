import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import geopandas as gpd

# Set config
st.set_page_config(page_title="Stadshagen Dashboard", layout="wide")

# Top Header
st.markdown("""
    <h1 style="font-size: 32px;">☀️ Solar Energy Flow in <span style='color:#ff9900;'>Stadshagen</span></h1>
    <p style="font-size: 18px; color: gray;">Current Situation</p>
""", unsafe_allow_html=True)

# Go back button
if st.button("⬅️ GO BACK"):
    st.switch_page("Home.py")

# Layout
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown("""
        <div style="background-color:#f2f2f2; padding:20px; border-radius:12px;">
            <h4>Solar Production</h4>
            <img src="https://via.placeholder.com/200x80/FFDD99/000000?text=Prod+Chart" width="100%">

            <h4>Solar Consumption</h4>
            <img src="https://via.placeholder.com/200x80/FFCCCC/000000?text=Cons+Chart" width="100%">

            <h4>Carbon Monitor</h4>
            <img src="https://via.placeholder.com/200x80/CCE5FF/000000?text=Carbon+Chart" width="100%">

            <br>
            <h4>Energy Flow</h4>
    """, unsafe_allow_html=True)

    # Simulated data
    dates = pd.date_range("2021-01-01", "2021-01-17")
    data = pd.DataFrame({
        "Date": dates,
        "Production": [60 + i % 10 for i in range(17)],
        "Consumption": [40 + i % 5 for i in range(17)],
        "Intended": [70 for _ in range(17)]
    })

    st.line_chart(data.set_index("Date"), use_container_width=True)

    st.selectbox("Select Month", ["Jan 2021"], index=0)

    if st.button("🚀 GO TO SIMULATION"):
        st.info("Simulation module is coming soon!")

    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Load and filter shapefile
    gdf = gpd.read_file("data/zwolle_districts.shp").to_crs(epsg=4326)
    gdf = gdf[gdf['OMSCHR'].str.contains("Stadshagen", case=False)]

    # Create zoomed-in map
    m = folium.Map(location=[52.54, 6.06], zoom_start=13)

    folium.GeoJson(
        data=gdf.geometry.__geo_interface__,
        name="Stadshagen",
        style_function=lambda x: {
            "fillColor": "#ffcc00",
            "color": "black",
            "weight": 3,
            "fillOpacity": 0.3,
        },
    ).add_to(m)

    st_folium(m, width=600, height=550)
