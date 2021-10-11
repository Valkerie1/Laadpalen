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

histogram_selector = st.selectbox('Graph to display:',['Charging time','Connected time'], index=0) 
fighist = go.Figure()
if histogram_selector == 'Charging time':
         laadtijd_rangeselection_max = st.slider('Select the charging time to display:',0,4000,600,100)
         laadtijd_rangeselection_min = 0
         
         
         fighist.add_trace(go.Histogram(histfunc='count', x=df_laadpaal_tijden['ChargeTime'], nbinsx=100))
         
         fighist.update_layout(title_text='The distribution of charging times',
                               title={'x':0.5, 'xanchor': 'center'},
                               xaxis_title='Charging time in minutes',
                               yaxis_title='Number of observations')

         st.plotly_chart(fighist)
elif histogram_selector == 'Connected time':
         connected_rangeselection_max = st.slider('Select the Connected time to display:',0,4000,600,100)
         connected_rangeselection_min = 0
         
         fighist.add_trace(go.Histogram(histfunc='count', x=df_laadpaal_tijden['ConnectedTime'], nbinsx=100))

         
         fighist.update_layout(title_text='The distribution of connected times',
                               title={'x':0.5, 'xanchor': 'center'},
                               xaxis_title='Connected time in minutes',
                               yaxis_title='Number of observatio
                               
         st.plotly_chart(fighist)
 













