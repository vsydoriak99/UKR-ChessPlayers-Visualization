from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd 
import requests
import urllib.request as urlreq


#Get excel file from chess-result for Only finished tournaments (malualy)
file = r'data\TournamentSearch_ukr_2021.xls'
df = pd.read_excel(file, skiprows=3)
df.to_csv('tournamentres.csv')
print(df.head())

def getStartURL(tournamentID, lan=1):
    url = f'http://chess-results.com/tnr{tournamentID}.aspx?lan={lan}&zeilen=0&prt=4&excel=2010'
    return url

def createURLForRes(tournamentID, round, lan = 1):
    url = f'http://chess-results.com/tnr{tournamentID}.aspx?lan={lan}&zeilen=0&art=1&rd={round}&prt=4&excel=2010'
    return url

def getAllData(df):
    general_df= DataFrame()
    for index, row in df.iterrows():
        res_table = getResltTable(row)
        st_table =getStartTable(row)
        result = pd.merge(res_table, st_table, how='left', on='Name')
        general_df = general_df.append(result)
    return general_df

def getResltTable(row):
    destination = 'temp.xls'
    key =row['DB-Key'] 
    rd = row['Rd']
    url = createURLForRes(key , rd)
    urlreq.urlretrieve(url, destination)
    raw_data = pd.read_excel(destination, header=None)

    header_idx, footer_idx = getHeadFootIndex(raw_data)

    clean_data  = pd.read_excel(destination, skiprows=header_idx, nrows = footer_idx - header_idx-2)
    clean_data.insert(1,'tr_key', key)
    return clean_data

def getStartTable(row):
    destination = 'temp_start.xls'
    key =row['DB-Key'] 
    url = getStartURL(key )
    urlreq.urlretrieve(url, destination)
    raw_data = pd.read_excel(destination, header=None)
    header_idx, footer_idx = getStartHeadFootIndex(raw_data)
    
    
    head = pd.read_excel(destination, skiprows=header_idx, nrows = 1)
    cols = ['Name']
    if 'FideID'in head.columns:
        cols.append('FideID')
    clean_data  = pd.read_excel(destination, usecols=cols, skiprows=header_idx, nrows = footer_idx - header_idx-2)

    return clean_data

def getStartHeadFootIndex(raw_data):
    header_idx = raw_data[raw_data[0].eq('No.')].index.values[0]
    footer_idx = raw_data[raw_data[0].eq('Chess-Tournament-Results-Server: Chess-Results')].index.values[0]
    return header_idx, footer_idx

def getHeadFootIndex(raw_data):
    header_idx = raw_data[raw_data[0].eq('Rk.')].index.values[0]
    footer_idx = raw_data[raw_data[0].eq('Annotation')].index.values[0]
    return header_idx, footer_idx



print(df.info())
allData = getAllData(df)
allData.to_csv('data\generalDF.csv')


