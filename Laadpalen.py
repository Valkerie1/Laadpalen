import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static

df = gpd.read_file('countries.geojson')
df1 = pd.read_csv('Life_Expectancy_Data.csv')

#df_who = df.merge(df1, left_on='ADMIN', right_on='Country')
#df_who = df1

#st.table(df1)

m = folium.Map(tiles='https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', 
               attr='Mapbox attribution')

folium.Choropleth(geo_data=df, name='geometry', 
                  data=df1, columns=['Country','GDP'], 
                  key_on='feature.geometry', 
                  fill_color='RdYlGn',
                  fill_opacity=1, 
                  line_opacity=0.7).add_to(m)

folium.features.ClickForMarker(popup=None).add_to(m)

folium_static(m)

