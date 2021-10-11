import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px

from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)


df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                   dtype={"fips": str})



df = px.data.election()
geojson = px.data.election_geojson()

fig = px.choropleth_mapbox(df, geojson=geojson, color="winner",
                           locations="district", featureidkey="properties.district",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)
dropdown_buttons = [
    {'method': 'update', 'label': 'All','args': [{'visible': [True, True, True]}]},
    {'method': 'update', 'label': 'Joly','args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': 'Coderre','args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': 'Bergeron','args': [{'visible': [False, False, True]}]}]

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})


st.plotly_chart(fig)

