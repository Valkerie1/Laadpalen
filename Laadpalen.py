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
         st.write('test')
         sidebar_keuze = st.radio('Kies een hoofdstuk:', ['Algemeen',"Elektrische auto's",'Laadpaal kaart'])
         
if sidebar_keuze == 'Laadpaal kaart':
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
         
         kaart_opties = st.selectbox('Kies een provincie:', ['Nederland','Gelderland','Fryslân','Zuid-Holland','Overijssel','Noord-Brabant','Groningen','Limburg','Noord-Holland','Zeeland','Utrecht','Flevoland','Drenthe'])
         
         if kaart_opties == 'Nederland':
                  a = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7,tiles='cartodbpositron')

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
                  
         if kaart_opties == 'Gelderland':
                  st.empty()
                  
         if kaart_opties == 'Fryslân':
                  st.empty()
                  
         if kaart_opties == 'Zuid-Holland':
                  st.empty()
                  
         if kaart_opties == 'Overijssel':
                  st.empty()
                  
         if kaart_opties == 'Noord-Brabant':
                  st.empty()
                  
         if kaart_opties == 'Groningen':
                  st.empty()
                  
         if kaart_opties == 'Limburg':
                  st.empty()
             
         if kaart_opties == 'Noord-Brabant':
                  st.empty()
                  
         if kaart_opties == 'Groningen':
                  st.empty()
                  
         if kaart_opties == 'Limburg':
                  st.empty()
                  
         if kaart_opties == 'Noord-Holland':
                  st.empty()
                  
         if kaart_opties == 'Zeeland':
                  st.empty()
                  

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
         fig.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]},xaxis = 0.3, yaxis = 1.2)
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















'''
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

with st.sidebar:
         st.write('test')
         sidebar_keuze = st.radio('Kies een hoofdstuk:', ['Algemeen',"Elektrische auto's",'Laadpaal kaart'])
         
if sidebar_keuze == 'Laadpaal kaart':
         b = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7, tiles='cartodbpositron')
         
         folium.Choropleth(
                  geo_data= gem_geo,
                  name= 'geometry',
                  data= gem_geo,
                  columns=['gemeentenaam', 'Oplaadpunten/km^2'],
                  key_on='feature.properties.gemeentenaam',
                  fill_color= 'Greens',
                  fill_opacity= 0.5,
                  line_opacity= 1.0,
                  legend_name= 'Oplaadpunten per km^2'
                  ).add_to(b)
         
         folium.Choropleth(
                  geo_data= prov_geo,
                  name= 'geometry',
                  fill_opacity= 0,
                  line_opacity= 0.8,
                  line_color= 'red'
                  ).add_to(b)
         folium_static(b) 
         


st.markdown("<h1 style='text-align: center; color: black;'>Personen voertuigen in Nederland</h1>", unsafe_allow_html=True)
st.write('''

''')
st.markdown('***')
st.markdown("<h3 style='text-align: center; color: black;'>Aantal voertuigen per brandstofsoort</h3>", unsafe_allow_html=True)
st.markdown('***')

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



# laadpaal data, laadtijden selecteren en naar minuten zetten

df_laadpaal_tijden = pd.DataFrame(datalaadpaal['ConnectedTime']*60)
df_laadpaal_tijden['ChargeTime'] = datalaadpaal['ChargeTime']*60
#df_laadpaal_tijden.describe()

df_laadpaal_tijden_to_delete = df_laadpaal_tijden[df_laadpaal_tijden['ChargeTime']<0].index
df_laadpaal_tijden.drop(df_laadpaal_tijden_to_delete, inplace=True)

# histogram
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
                  

# lijn grafiek

# laad de van de rdw
#df_line = pd.read_csv('Lijngrafiek2.2.csv')
#df_line['Datum eerste afgifte Nederland'] =  pd.to_datetime(df_line['Datum eerste afgifte Nederland'], format='%Y-%m-%d')
#df_line = df_line.drop(columns='Aantal')
#df_pivot = pd.pivot_table(df_line, index='Datum eerste afgifte Nederland', columns='ID', fill_value=0)
#df_pivot.columns = ['_'.join(str(s).strip() for s in col if s) for col in df_pivot.columns]
#df_pivot = df_pivot.drop(columns=['cumsum_G', 'cumsum_H'])
#df_pivot = df_pivot.reset_index()
#df_pivot.info()
#df_pivot.columns = ['Datum eerste afgifte Nederland', 'Benzine', 'Diesel', 'Elektriciteit', 'LPG', 'Alcohol', 'CNG']
# data opslaan naar een eigen csv bestand
#df_pivot.to_csv('lijngrafiek_data.csv')

df_pivot = pd.read_csv('lijngrafiek_data.csv')

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
fig.update_layout({'updatemenus':[{'type': 'dropdown', 'buttons': dropdown_buttons}]})
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


# kaart
st.write('***')
st.markdown("<h4 style='text-align: center; color: black;'>Oplaadpunten per vierkante kilometer</h4>", unsafe_allow_html=True)
st.write('***')
         
#inladen data grenzen Nederland
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

#map maken
a = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7,tiles='cartodbpositron')

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

b = folium.Map(location=[52.0893191, 5.1101691], zoom_start= 7, tiles='cartodbpositron')
         
folium.Choropleth(
    geo_data= gem_geo,
    name= 'geometry',
    data= gem_geo,
    columns=['gemeentenaam', 'Oplaadpunten/km^2'],
    key_on='feature.properties.gemeentenaam',
    fill_color= 'Greens',
    fill_opacity= 0.5,
    line_opacity= 1.0,
    legend_name= 'Oplaadpunten per km^2'
).add_to(b)
         
folium.Choropleth(
    geo_data= prov_geo,
    name= 'geometry',
    fill_opacity= 0,
    line_opacity= 0.8,
    line_color= 'red'
).add_to(b)


col1, col2, col3 = st.columns([2,6,1])

with col2:
         folium_static(a)
         folium_static(b)           
'''         
 













