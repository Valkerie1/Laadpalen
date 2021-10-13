import streamlit as st
import folium
import geopandas as gpd
import pandas as pd
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import requests
import json
import plotly.figure_factory as ff
import scipy
from shapely.geometry import Point

st.set_page_config(page_title = 'Streamlit Dashboard', layout= 'wide')

# laden van api
countrycode = 'NL'
url = 'https://api.openchargemap.io/v3/poi/?output=json&countrycode='+str(countrycode)+'&opendata=true&maxresults=10000&key=15c7cb5b-1cda-4a8d-ba93-14db688bf993'
r=requests.get(url)
datatxt= r.text
datajs = json.loads(datatxt)
data = pd.json_normalize(datajs)

# laden van rdw data

RDW_compleet=pd.read_csv('RDW_compleet.csv')

# laden van laadpaal data

datalaadpaal = pd.read_csv('laadpaaldata.csv')

# opschonen api data

labels = ['UserComments', 'PercentageSimilarity','MediaItems','IsRecentlyVerified','DateLastVerified',
         'UUID','ParentChargePointID','DataProviderID','DataProvidersReference','OperatorID',
         'OperatorsReference','UsageTypeID','GeneralComments','DatePlanned','DateLastConfirmed','MetadataValues',
         'SubmissionStatusTypeID','DataProvider.WebsiteURL','DataProvider.Comments','DataProvider.DataProviderStatusType.IsProviderEnabled',
         'DataProvider.DataProviderStatusType.ID','DataProvider.DataProviderStatusType.Title',
         'DataProvider.IsRestrictedEdit','DataProvider.IsOpenDataLicensed','DataProvider.IsApprovedImport',
         'DataProvider.License','DataProvider.DateLastImported','DataProvider.ID','DataProvider.Title',
         'OperatorInfo.Comments','OperatorInfo.PhonePrimaryContact','OperatorInfo.PhoneSecondaryContact',
         'OperatorInfo.IsPrivateIndividual','OperatorInfo.AddressInfo','OperatorInfo.BookingURL',
         'OperatorInfo.ContactEmail','OperatorInfo.FaultReportEmail','OperatorInfo.IsRestrictedEdit',
         'UsageType','OperatorInfo','AddressInfo.DistanceUnit','AddressInfo.Distance','AddressInfo.AccessComments',
         'AddressInfo.ContactEmail','AddressInfo.ContactTelephone2','AddressInfo.ContactTelephone1',
         'OperatorInfo.WebsiteURL','OperatorInfo.ID','UsageType.ID','StatusType.IsUserSelectable',
         'StatusType.ID','SubmissionStatus.IsLive','SubmissionStatus.ID','SubmissionStatus.Title',
         'AddressInfo.CountryID','AddressInfo.Country.ContinentCode','AddressInfo.Country.ID',
         'AddressInfo.Country.ISOCode','AddressInfo.RelatedURL','Connections']
data = data.drop(columns=labels)

data_town = data['AddressInfo.Town']
#data_town.value_counts()

data_status = data['AddressInfo.StateOrProvince']
#data_status.value_counts()

data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Drente', 'Drenthe')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Samenwerkingsverband Regio Eindhoven', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord Holand ', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('FRL', 'Friesland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('GLD', 'Gelderland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Stellendam', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('UT', 'Utrecht')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Regio Twente', 'Overijssel')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Stadsregio Rotterdam', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord Brabant', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Regio Zwolle', 'Overijssel')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('UTRECHT', 'Utrecht')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Seeland', 'Zeeland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord Brabant', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord-Hooland', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Stadsregio Arnhem Nijmegen', 'Gelderland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('North-Holland', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Overijsel', 'Overijssel')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Nordbrabant', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('MRDH', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Nordholland', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Flevolaan', 'Flevoland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Stadsregio Amsterdam', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('ZH', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Zuid Holland', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('NH', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('North Holland', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('South Holland', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Stadsgewest Haaglanden', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('North Brabant', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord Holland', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Zuid-Holland ', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord Holand', 'Noord-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Noord-Brabant ', 'Noord-Brabant')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Zuid-Holland ', 'Zuid-Holland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Gelderland ', 'Gelderland')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('UtrechtRECHT', 'Utrecht')
data['AddressInfo.StateOrProvince'] = data['AddressInfo.StateOrProvince'].str.replace('Holandia Północna', 'Noord-Holland')

#data['AddressInfo.StateOrProvince'].unique()

data_status = data['AddressInfo.StateOrProvince']
#data_status.value_counts()

data_empty_town = data_town.isna()
#data_empty_town.value_counts()

data_empty = data_status.isna()
#data_empty.value_counts()



# opschonen rdw data

#labelsrdw=['API Gekentekende_voertuigen_voertuigklasse','API Gekentekende_voertuigen_carrosserie_specifiek',
#          'API Gekentekende_voertuigen_carrosserie','API Gekentekende_voertuigen_brandstof','API Gekentekende_voertuigen_assen',
#          'API Gekentekende_voertuigen_assen','Maximum ondersteunende snelheid','Aantal rolstoelplaatsen',
#          'Maximum massa samenstelling','Openstaande terugroepactie indicator','Export indicator',
#          'Wielbasis','Vermogen massarijklaar','Volgnummer wijziging EU typegoedkeuring','Uitvoering',
#          'Variant','Typegoedkeuringsnummer','Type gasinstallatie','Type','Plaats chassisnummer',
#          'Europese uitvoeringcategorie toevoeging','Europese voertuigcategorie toevoeging',
#          'Europese voertuigcategorie','Afwijkende maximum snelheid','Afstand voorzijde voertuig tot hart koppeling',
#          'Afstand hart koppeling tot achterzijde voertuig','Aantal wielen','Aantal deuren','Aantal staanplaatsen',
#          'Vermogen (brom/snorfiets)','Aanhangwagen middenas geremd','Aanhangwagen autonoom geremd',
#          'Oplegger geremd','Laadvermogen','Maximale constructiesnelheid (brom/snorfiets)','WAM verzekerd',
#          'Wacht op keuren','Zuinigheidslabel','Maximum trekken massa geremd','Maximum massa trekken ongeremd','Cilinderinhoud',
#          'Aantal cilinders','Tweede kleur','Bruto BPM','Voertuigsoort']
#datardw = datardw.drop(columns=labelsrdw)

#RDW_totaal = pd.read_csv('Open_Data_RDW__Gekentekende_voertuigen.csv')
#RDW_kenteken_datum = RDW_totaal[['Kenteken', 'Datum tenaamstelling']]
#RDW_compleet = datardw.merge(RDW_kenteken_datum, on='Kenteken', how='left')
#RDW_compleet[RDW_compleet['Datum tenaamstelling'].isna()]
#RDW_compleet['Datum tenaamstelling'] = pd.to_datetime(RDW_compleet['Datum tenaamstelling'], format='%Y%m%d')

df_pivot = pd.read_csv('lijngrafiek_data.csv')






# interactive onderdelen
with st.sidebar:
         sidebar_keuze = st.radio('Kies een hoofdstuk:', ['Algemeen',"Elektrische auto's",'Laadpaal kaart','Bronnen', 'Credits'])
         
if sidebar_keuze == 'Laadpaal kaart':
         st.markdown('***')
         st.markdown("<h3 style='text-align: center; color: black;'>Aantal laadpalen per vierkante meter</h3>", unsafe_allow_html=True)
         st.markdown('***')
         
         grens= gpd.read_file('bestuurlijkegrenzen.gpkg', layer= 'landsgrens')
         provincies= gpd.read_file('bestuurlijkegrenzen.gpkg', layer= 'provincies')
         gemeente = gpd.read_file('bestuurlijkegrenzen.gpkg', layer= 'gemeenten')


         #Data omzetten in point
         data['coordinates'] = data.apply(lambda x: Point(x['AddressInfo.Longitude'], x['AddressInfo.Latitude']), axis=1)

         #panda dataframe naar geopandas
         geodata = gpd.GeoDataFrame(data, geometry= 'coordinates')

         #crs waardes veranderen zodat deze gelijk zijn (4326 want is voor latitude en longitude) 
         geodata.set_crs(epsg= 4326, inplace=True)
         provincies.to_crs(epsg= 4326, inplace= True)

         merge= gpd.sjoin(geodata, provincies)
         prov_data= merge.groupby('provincienaam', as_index=False).sum()

         #Omzetten crs zodat berekening Area makkelijker naar km^2 gaat (28992 want is origineel)
         provincies.to_crs(epsg= 28992, inplace= True)
         provincies['Area']= provincies.geometry.area / 10 ** 6

         #Alle data mergen in een dataframe
         prov_data= prov_data.merge(provincies, on= 'provincienaam')

         #Data die nodig is eruit filteren
         prov_data= prov_data[['provincienaam', 'NumberOfPoints', 'geometry', 'Area']]
         prov_data['Oplaadpunten/km^2'] = prov_data['NumberOfPoints']/prov_data['Area']

         #Als prov_data niet werkt in choropleth kan je omzetten naar geopandas met deze code
         prov_geo= gpd.GeoDataFrame(prov_data, geometry= 'geometry')

         #crs waardes veranderen zodat deze gelijk zijn (4326 want is voor latitude en longitude) 
         gemeente.to_crs(epsg= 4326, inplace= True)
         merge2= gpd.sjoin(geodata, gemeente)
         gem_data= merge2.groupby('gemeentenaam', as_index=False).sum()
         gemeente.to_crs(epsg= 28992, inplace= True)
         gemeente['Area']= gemeente.geometry.area / 10 ** 6
         gem_data= gem_data.merge(gemeente, on= 'gemeentenaam')
         gem_data= gem_data[['gemeentenaam', 'NumberOfPoints', 'geometry', 'Area']]
         gem_data['Oplaadpunten/km^2'] = gem_data['NumberOfPoints']/gem_data['Area']

         #Als gem_data niet werkt in choropleth kan je omzetten naar geopandas met deze code
         gem_geo= gpd.GeoDataFrame(gem_data, geometry= 'geometry')
         
         merge3= gpd.sjoin(gem_geo, provincies, op= 'within')
         merge3= merge3[['gemeentenaam', 'NumberOfPoints', 'geometry', 'provincienaam', 'Oplaadpunten/km^2']]
         zuid_holland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Zuid-Holland'], geometry= 'geometry')
         noord_brabant= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Noord-Brabant'], geometry= 'geometry')
         gelderland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Gelderland'], geometry= 'geometry')
         drenthe= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Drenthe'], geometry= 'geometry')
         groningen= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Groningen'], geometry= 'geometry')
         noord_holland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Noord-Holland'], geometry= 'geometry')
         friesland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Fryslân'], geometry= 'geometry')
         overijssel= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Overijssel'], geometry= 'geometry')
         flevoland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Flevoland'], geometry= 'geometry')
         utrecht= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Utrecht'], geometry= 'geometry')
         limburg= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Limburg'], geometry= 'geometry')
         zeeland= gpd.GeoDataFrame(merge3[merge3['provincienaam'] == 'Zeeland'], geometry= 'geometry')
         
         kaart_opties = st.selectbox('Kies een provincie:', ['Nederland','Gelderland','Fryslân','Zuid-Holland','Overijssel','Noord-Brabant','Groningen','Limburg','Noord-Holland','Zeeland','Utrecht','Flevoland','Drenthe'])
         
         if kaart_opties == 'Nederland':
                  a = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7,tiles='cartodbpositron')
                  style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
                  highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
                  Info_prov = folium.features.GeoJson(
                           prov_geo,
                           style_function=style_function, 
                           highlight_function=highlight_function, 
                           tooltip=folium.features.GeoJsonTooltip(
                           fields=['provincienaam', 'NumberOfPoints', 'Oplaadpunten/km^2'],
                           aliases=['Provincie: ','Aantal Laadpalen: ', 'Oplaadpunten/km^2: '],
                           style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
                           )
                           )
                  a.add_child(Info_prov)

                  folium.Choropleth(
                  geo_data= prov_geo,
                  name= 'geometry',
                  data= prov_geo,
                  columns=['provincienaam', 'Oplaadpunten/km^2'],
                  key_on='feature.properties.provincienaam',
                  fill_color= 'Greens',
                  fill_opacity= 0.5,
                  line_opacity= 0.8,
                  legend_name= 'Oplaadpunten per km^2'
                  ).add_to(a)

                  folium.Choropleth(
                  geo_data= grens,
                  name= 'geometry',
                  fill_opacity= 0,
                  line_opacity= 0.8,
                  line_color= 'red'
                  ).add_to(a)
                  folium_static(a)
                  
         if kaart_opties == 'Gelderland':
                  Gelderland= folium.Map(location=[52.18208950171327, 5.880307820690871], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= gelderland,
                           name= 'geometry',
                           data= gelderland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Gelderland)
                  folium_static(Gelderland)
                  
         if kaart_opties == 'Fryslân':
                  Friesland= folium.Map(location=[53.17625169811117, 5.718895926104773], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= friesland,
                           name= 'geometry',
                           data= friesland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Friesland)
                  folium_static(Friesland)
                  
         if kaart_opties == 'Zuid-Holland':
                  Zuid_holland= folium.Map(location=[52.030720657702716, 4.428187281122106], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= zuid_holland,
                           name= 'geometry',
                           data= zuid_holland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Zuid_holland)
                  folium_static(Zuid_holland)
                  
         if kaart_opties == 'Overijssel':
                  Overijssel= folium.Map(location=[52.43894167549349, 6.458229214773575], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= overijssel,
                           name= 'geometry',
                           data= overijssel,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Overijssel)
                  folium_static(Overijssel)
                  
         if kaart_opties == 'Noord-Brabant':
                  Noord_brabant= folium.Map(location=[51.57758163943472, 5.013135901291934], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= noord_brabant,
                           name= 'geometry',
                           data= noord_brabant,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Noord_brabant)
                  folium_static(Noord_holland)
                  
         if kaart_opties == 'Groningen':
                  Groningen= folium.Map(location=[53.179018023746366, 6.665667745346082], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= groningen,
                           name= 'geometry',
                           data= groningen,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Groningen)
                  folium_static(Groningen)
                  
         if kaart_opties == 'Limburg':
                  Limburg= folium.Map(location=[51.193685827757744, 6.066756954225762], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= limburg,
                           name= 'geometry',
                           data= limburg,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Limburg)
                  folium_static(Limburg)
             
         if kaart_opties == 'Drenthe':
                  Drenthe= folium.Map(location=[52.881122487230954, 6.610381065662523], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= drenthe,
                           name= 'geometry',
                           data= drenthe,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Drenthe)
                  folium_static(Drenthe)
                  
         if kaart_opties == 'Flevoland':
                  Flevoland= folium.Map(location=[52.51375325413512, 5.637642228959302], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= flevoland,
                           name= 'geometry',
                           data= flevoland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Flevoland)
                  folium_static(Flevoland)
                  
         if kaart_opties == 'Utrecht':
                  Utrecht= folium.Map(location=[52.12161941836688, 5.20694784788699], zoom_start= 10,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= utrecht,
                           name= 'geometry',
                           data= utrecht,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Utrecht)
                  folium_static(Utrecht)
                  
         if kaart_opties == 'Noord-Holland':
                  Noord_holland= folium.Map(location=[52.616569744852114, 4.842259719854058], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= noord_holland,
                           name= 'geometry',
                           data= noord_holland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Noord_holland)
                  folium_static(Noord_holland)
                  
         if kaart_opties == 'Zeeland':
                  Zeeland= folium.Map(location=[51.4799479729807, 3.8654951754026565], zoom_start= 9,tiles='cartodbpositron')
                  folium.Choropleth(
                           geo_data= zeeland,
                           name= 'geometry',
                           data= zeeland,
                           columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                           key_on='feature.properties.gemeentenaam',
                           fill_color= 'PuBuGn',
                           fill_opacity= 0.5,
                           line_opacity= 0.8,
                           legend_name= 'Oplaadpunten/km^2'
                           ).add_to(Zeeland)
                  folium_static(Zeeland)
                  

elif sidebar_keuze == 'Algemeen':
         df_pivot = pd.read_csv('lijngrafiek_data.csv')

         st.markdown('***')
         st.markdown("<h3 style='text-align: center; color: black;'>Aantal voertuigen per brandstofsoort</h3>", unsafe_allow_html=True)
         st.markdown('***')
         col1, col2, col3, col4, col5, col6 = st.columns(6)

         col1.markdown("<h5 style='text-align: center; color: black;'>Benzine voertuigen</h5>", unsafe_allow_html=True)
         col1.markdown("<h5 style='text-align: center; color: black;'>8.02 M</h5>", unsafe_allow_html=True)

         col2.markdown("<h5 style='text-align: center; color: black;'>Diesel voertuigen</h5>", unsafe_allow_html=True)
         col2.markdown("<h5 style='text-align: center; color: black;'>1.12 M</h5>", unsafe_allow_html=True)

         col3.markdown("<h5 style='text-align: center; color: black;'>Elektrische voertuigen</h5>", unsafe_allow_html=True)
         col3.markdown("<h5 style='text-align: center; color: black;'>683 k</h5>", unsafe_allow_html=True)

         col4.markdown("<h5 style='text-align: center; color: black;'>LPG voertuigen</h5>", unsafe_allow_html=True)
         col4.markdown("<h5 style='text-align: center; color: black;'>119 k</h5>", unsafe_allow_html=True)

         col5.markdown("<h5 style='text-align: center; color: black;'>Alcohol voertuigen</h5>", unsafe_allow_html=True)
         col5.markdown("<h5 style='text-align: center; color: black;'>9 k</h5>", unsafe_allow_html=True)

         col6.markdown("<h5 style='text-align: center; color: black;'>CNG voertuigen</h5>", unsafe_allow_html=True)
         col6.markdown("<h5 style='text-align: center; color: black;'>4 k</h5>", unsafe_allow_html=True)

         st.markdown("***")
         
         fig = px.line(df_pivot, x="Datum eerste afgifte Nederland", y=df_pivot.columns,
                  title='Aantal autos per brandstofsoort per maand', log_y=True)

         dropdown_buttons = [
         {'method': 'update', 'label': 'Alle brandstofsoorten','args': [{'visible': [True, True, True, True, True, True]}]},
         {'method': 'update', 'label': 'Benzine','args': [{'visible': [True, False, False, False, False, False]}]},
         {'method': 'update', 'label': 'Diesel','args': [{'visible': [False, True, False, False, False, False]}]},
         {'method': 'update', 'label': 'Elektriciteit','args': [{'visible': [False, False, True, False, False, False]}]},
         {'method': 'update', 'label': 'LPG','args': [{'visible': [False, False, False, True, False, False]}]},
         {'method': 'update', 'label': 'Alcohol','args': [{'visible': [False, False, False, False, True, False]}]},
         {'method': 'update', 'label': 'CNG','args': [{'visible': [False, False, False, False, False, False, True]}]}]
         fig.update_layout(updatemenus=[go.layout.Updatemenu(buttons=dropdown_buttons, x = 1.01, xanchor = 'left',
         y = 0.5, yanchor = 'top',)])
         fig.update_layout(legend_title_text='Brandstofsoorten')
         fig.update_layout(yaxis_title="Totaal aantal auto's")
         fig.update_layout(
         title={
         'text': "Cumulatieve som aantal auto's per brandstofsoort per maand",
         'xanchor': 'center',
         'x': 0.5,
         'yanchor': 'top'})
         fig.update_layout(
             xaxis=dict(
         rangeselector=dict(
                  buttons=list([
                  dict(label="Compleet",
                     step="all"),
                  dict(count=80,
                     label="80j",
                     step="year",
                     stepmode="backward"),
                  dict(count=70,
                     label="70j",
                     step="year",
                     stepmode="backward"),
                  dict(count=60,
                     label="60j",
                     step="year",
                     stepmode="backward"),
                  dict(count=50,
                     label="50j",
                     step="year",
                     stepmode="backward"),
                  dict(count=40,
                     label="40j",
                     step="year",
                     stepmode="backward"),
                  dict(count=30,
                     label="30j",
                     step="year",
                     stepmode="backward"),
                  dict(count=20,
                     label="20j",
                     step="year",
                     stepmode="backward"),
                  dict(count=10,
                     label="10j",
                     step="year",
                     stepmode="backward"),
                  dict(count=1,
                     label="1j",
                     step="year",
                     stepmode="backward"),
                  dict(count=1,
                     label="Jaar tot op heden",
                     step="year",
                     stepmode="todate"),
                  ])
                  ),
                  rangeslider=dict(
                           visible=True
                  ),
                  type="date"
                  )
                  )
         fig.update_traces(connectgaps=True)

         st.plotly_chart(fig)
elif sidebar_keuze == "Elektrische auto's":
         st.markdown('***')
         st.markdown("<h3 style='text-align: center; color: black;'>Laad gedrag voor eleketrische auto's in Nederland</h3>", unsafe_allow_html=True)
         st.markdown('***')
         
         # laadpaal data, laadtijden selecteren en naar minuten zetten

         df_laadpaal_tijden = pd.DataFrame(datalaadpaal['ConnectedTime']*60)
         df_laadpaal_tijden['ChargeTime'] = datalaadpaal['ChargeTime']*60
         #df_laadpaal_tijden.describe()

         df_laadpaal_tijden_to_delete = df_laadpaal_tijden[df_laadpaal_tijden['ChargeTime']<0].index
         df_laadpaal_tijden.drop(df_laadpaal_tijden_to_delete, inplace=True)

         with st.expander('Opties:'):
                  laadtijd_rangeselection_max = st.slider('Selecteer het bereik van de oplaad tijd:',0,4000,600,100)
                  laadtijd_selectbox = st.selectbox('Laat opmerkingen zien:', ['Gemiddelde','Mediaan','Beide','Geen'], index=3, key='laadtijd_selectbox')
         laadtijd_rangeselection_min = 0
         
         fighist = go.Figure()
         fighist.add_trace(go.Histogram(histfunc='count', x=df_laadpaal_tijden['ChargeTime'], nbinsx=180))
         fighist.update_layout(title_text='Verdeling van oplaad tijden',
                               title={'x':0.5, 'xanchor': 'center'},
                               xaxis_title='Oplaad tijd in minuten',
                               yaxis_title='Aantal observaties',
                               xaxis={'range':[laadtijd_rangeselection_min,laadtijd_rangeselection_max]} )
         
         if laadtijd_selectbox == 'Beide':
                  fighist.update_layout(annotations=[{
                                    'x':df_laadpaal_tijden['ChargeTime'].mean(),
                                    'y':1125,
                                    'ax':35,
                                    'ay':-30,
                                    'text':'Mean = 149',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}},
                                    
                                    {'x':df_laadpaal_tijden['ChargeTime'].median(),
                                    'y':1125,
                                    'ax':-20,
                                    'ay':-50,
                                    'text':'Median = 134',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist)
         elif laadtijd_selectbox == 'Gemiddelde':
                  fighist.update_layout(annotations=[{
                                    'x':df_laadpaal_tijden['ChargeTime'].mean(),
                                    'y':1125,
                                    'ax':0,
                                    'ay':-30,
                                    'text':'Mean = 149',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist)
         elif laadtijd_selectbox == 'Mediaan':
                  fighist.update_layout(annotations=[{'x':df_laadpaal_tijden['ChargeTime'].median(),
                                    'y':1125,
                                    'ax':0,
                                    'ay':-30,
                                    'text':'Median = 134',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist)
         elif laadtijd_selectbox == 'Geen':
                  st.plotly_chart(fighist)

         with st.expander('Options'):
                  connected_rangeselection_max = st.slider('Selecteer het bereik van de tijd aan de laadpaal:',0,4000,1600,100)
                  connected_selectbox = st.selectbox('Laat opmerkingen zien:', ['Gemiddelde','Mediaan','Beide', 'Geen'], index=3, key='connected_selectbox')
         connected_rangeselection_min = 0
         fighist2 = go.Figure()        
         fighist2.add_trace(go.Histogram(histfunc='count', x=df_laadpaal_tijden['ConnectedTime'], nbinsx=220))
         fighist2.update_layout(title_text='Verdeling van tijd verbonden aan de laadpaal',
                               title={'x':0.5, 'xanchor': 'center'},
                               xaxis_title='Verbonden tijd in minuten',
                               yaxis_title='Aantal observaties',
                               xaxis={'range':[connected_rangeselection_min,connected_rangeselection_max]})
                               
         if connected_selectbox == 'Beide':
                  fighist2.update_layout(annotations=[{
                                    'x':df_laadpaal_tijden['ConnectedTime'].mean(),
                                    'y':260,
                                    'ax':0,
                                    'ay':-30,
                                    'text':'Mean = 381',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}},
                                    
                                    {'x':df_laadpaal_tijden['ConnectedTime'].median(),
                                    'y':765,
                                    'ax':10,
                                    'ay':-40,
                                    'text':'Median = 228',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist2)
         elif connected_selectbox == 'Gemiddelde':
                  fighist2.update_layout(annotations=[{
                                    'x':df_laadpaal_tijden['ConnectedTime'].mean(),
                                    'y':260,
                                    'ax':0,
                                    'ay':-30,
                                    'text':'Mean = 381',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist2)
         elif connected_selectbox == 'Mediaan':
                  fighist2.update_layout(annotations=[{'x':df_laadpaal_tijden['ConnectedTime'].median(),
                                    'y':765,
                                    'ax':10,
                                    'ay':-40,
                                    'text':'Median = 228',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
                  st.plotly_chart(fighist2)
         elif laadtijd_selectbox == 'Geen':
                  st.plotly_chart(fighist2)
                  
         with st.expander('Options'):
                  distplot_rangeselection_max = st.slider('Selecteer het bereik van de tijd aan de laadpaal:',0,4000,600,100)
         distplot_rangeselection_min = 0
         
         group_1 = df_laadpaal_tijden['ChargeTime']
         group_2 = df_laadpaal_tijden['ConnectedTime']
         data_distplot = [group_1, group_2]
         group_labels = ['Oplaad tijd','Tijd verbonden aan de laadpaal']
         
         figdistplot = ff.create_distplot(data_distplot, group_labels, colors=['rgb(235,52,52)','rgb(67,52,235)'])

         figdistplot.update_layout(title_text='Kansdichtheids functie van de oplaad tijd en tijd verbonden aan de laadpaal',
                                   title={'x':0.5, 'xanchor': 'center'},
                                   xaxis_title='Tijd in minuten',
                                   yaxis_title='Kans',
                                   xaxis={'range':[distplot_rangeselection_min,distplot_rangeselection_max]})
         st.plotly_chart(figdistplot)
         
elif sidebar_keuze == 'Bronnen':
         st.markdown('***')
         st.markdown("<h3 style='text-align: center; color: black;'>Bronnen</h3>", unsafe_allow_html=True)
         st.markdown('***')
         
         st.write(''' 
         
         RDW
         
         https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen/m9d7-ebf2
         
         https://opendata.rdw.nl/Voertuigen/Open-Data-RDW-Gekentekende_voertuigen_brandstof/8ys7-d773
         
         https://opendata.rdw.nl/Voertuigen/Elektrische-voertuigen/w4rt-e856
                  
         OpenChargeMap
         
         https://openchargemap.org/site/develop/api
         
         ''')
         
       
elif sidebar_keuze == 'Credits':
         st.markdown('***')
         st.markdown("<h3 style='text-align: center; color: black;'>Credits</h3>", unsafe_allow_html=True)
         st.markdown('***')
         
         st.markdown('''
         
        
         ''')


