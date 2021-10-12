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

st.set_page_config(page_title = 'Streamlit Dashboard', layout= 'wide')
st.markdown("<h1 style='text-align: center; color: black;'>Personen voertuigen in Nederland</h1>", unsafe_allow_html=True)

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
col1, col2, col3 = st.columns(3)

col1.markdown("<h1 style='text-align: center; color: black;'>Benzine voertuigen</h1>", unsafe_allow_html=True)
col1.markdown("<h1 style='text-align: center; color: black;'>8.02 M</h1>", unsafe_allow_html=True)
col2.markdown("<h1 style='text-align: center; color: black;'>Diesel voertuigen</h1>", unsafe_allow_html=True)
col3.markdown("<h1 style='text-align: center; color: black;'>Elektrische voertuigen</h1>", unsafe_allow_html=True)





histogram_selector = st.selectbox('Selecteer een grafiek:',['Laad tijd','Tijd aan de laadpaal', 'Kansdichtheid'], index=0) 

fighist = go.Figure()
if histogram_selector == 'Laad tijd':
         
         
         with st.expander('Opties:'):
                  col1, col2 = st.columns(2)
                  laadtijd_rangeselection_max = col1.slider('Selecteer het bereik van de oplaad tijd:',0,4000,600,100)
                  laadtijd_selectbox = col2.selectbox('Laat opmerkingen zien:', ['Gemiddelde','Mediaan','Beide'], index=2)
         laadtijd_rangeselection_min = 0
         
         
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
         
elif histogram_selector == 'Tijd aan de laadpaal':
         with st.expander('Options'):
                  col1, col2 = st.columns(2)
                  connected_rangeselection_max = col1.slider('Selecteer het bereik van de tijd aan de laadpaal:',0,4000,1600,100)
                  connected_selectbox = col2.selectbox('Laat opmerkingen zien:', ['Gemiddelde','Mediaan','Beide'], index=2)
         connected_rangeselection_min = 0

                 
         fighist.add_trace(go.Histogram(histfunc='count', x=df_laadpaal_tijden['ConnectedTime'], nbinsx=220))
         
         fighist.update_layout(title_text='Verdeling van tijd verbonden aan de laadpaal',
                               title={'x':0.5, 'xanchor': 'center'},
                               xaxis_title='Verbonden tijd in minuten',
                               yaxis_title='Aantal observaties',
                               xaxis={'range':[connected_rangeselection_min,connected_rangeselection_max]})
                               
         if connected_selectbox == 'Beide':
                  fighist.update_layout(annotations=[{
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
         elif connected_selectbox == 'Gemiddelde':
                  fighist.update_layout(annotations=[{
                                    'x':df_laadpaal_tijden['ConnectedTime'].mean(),
                                    'y':260,
                                    'ax':0,
                                    'ay':-30,
                                    'text':'Mean = 381',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])
         elif connected_selectbox == 'Mediaan':
                  fighist.update_layout(annotations=[{'x':df_laadpaal_tijden['ConnectedTime'].median(),
                                    'y':765,
                                    'ax':10,
                                    'ay':-40,
                                    'text':'Median = 228',
                                    'showarrow': True,
                                    'arrowhead':1,
                                    'arrowsize':2,
                                    'font':{'size':12}}])         
         st.plotly_chart(fighist)
        
elif histogram_selector == 'Kansdichtheid':
         distplot_rangeselection_max = st.slider('Selecteer het bereik van de tijd:',0,4000,600,100)
         distplot_rangeselection_min = 0
         
         group_1 = df_laadpaal_tijden['ChargeTime']
         group_2 = df_laadpaal_tijden['ConnectedTime']
         data = [group_1, group_2]
         group_labels = ['Oplaad tijd','Tijd verbonden aan de laadpaal']
         
         figdistplot = ff.create_distplot(data, group_labels, colors=['rgb(235,52,52)','rgb(67,52,235)'])

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


        
         
         
 













