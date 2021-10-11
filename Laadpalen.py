import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static

df = gpd.read_file('https://github.com/Valkerie1/Laadpalen/blob/main/countries.geojson')
df1 = pd.read_csv('https://github.com/Valkerie1/Laadpalen/blob/main/Life_Expectancy_Data.csv')

df_who = df.merge(df1, left_on='ADMIN', right_on='Country')
df_who.head()

m = folium.Map(tiles='https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', 
               attr='Mapbox attribution')

folium.Choropleth(geo_data=df_who, name='geometry', 
                  data=df_who, columns=['ADMIN','GDP'], 
                  key_on='feature.properties.Country', 
                  fill_color='RdYlGn',
                  fill_opacity=1, 
                  line_opacity=0.7).add_to(m)

folium.features.ClickForMarker(popup=None).add_to(m)

folium_static(m)
