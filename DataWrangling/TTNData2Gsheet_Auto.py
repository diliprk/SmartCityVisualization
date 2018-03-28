#### Reading Data from The Things Network Data and Automatically Storing it to a Google Spreadsheet

# Author: Dilip Rajkumar
# Email: d.rajkumar@hbksaar.de
# Date: 19/01/2018
# Revision: version#1
# License: MIT License

import pandas as pd
import requests
from df2gspread import df2gspread as d2g
import time

## Set Initial Time Duration in mins to query TTN Data:
time_duration = 5

# Insert spreadsheet file id of Google Spreadsheet
spreadsheet = '1ftXlebCTDp5tTxvlm5K3Sv1oNttDHR7s1xTi-i-ZR_o' ## Google SpreadSheet Title: TTN_Live_DataLogger
# Insert Sheet Name
wks_name = 'Sheet1'

def queryttndata(time_duration):
    ''' 
    This function queries data from TTN Swagger API based on a time duration which is given as an input
    '''
    headers = {'Accept': 'application/json','Authorization': 'key ttn-account-v2.P4kRaEqenNGbIdFSgSLDJGMav5K9YrekkMm_F1lOVrw'}
    ## Set query duration in minutes
    querytime = str(time_duration) + 'm'
    params = (('last', querytime),)
    response = requests.get('https://vehiclecounter.data.thethingsnetwork.org/api/v2/query', headers=headers, params=params).json()
    df_raw = pd.DataFrame.from_dict(response)
    return df_raw    

def cleandf(df):
    '''
    In this function we pass as input the raw dataframe from TTN in JSON format to clean and optimize the data.
    This function is customized and unique to every dataset
    '''
    df.rename(columns={'time': 'TTNTimeStamp'}, inplace=True)
    df['TTNTimeStamp'] = pd.to_datetime(df['TTNTimeStamp'])    
    df['TTNTimeStamp'] = df['TTNTimeStamp'] + pd.Timedelta(hours=1) ## Offset Time by 1 hour to fix TimeZone Error of Swagger API TimeStamps
    df['TTNTimeStamp'] = df['TTNTimeStamp'].values.astype('datetime64[s]')    
    drop_cols = ['raw','device_id']
    df = df.drop(drop_cols, 1)
    df.reset_index()
    df = df.reindex(['TTNTimeStamp','Count'], axis=1)
    print("Latest Data:")
    print(df.tail(1),'\n')
    return df

while True:  
    #begin your infinite loop    
    df_raw = queryttndata(time_duration)
    df_clean = cleandf(df_raw)    
    d2g.upload(df_clean, spreadsheet,wks_name,col_names=True,clean=True) # Write dataframe to Google Spreadsheet
    df_clean.to_csv('TTN_VehicleCountData.csv', date_format="%d/%m/%Y %H:%M:%S",index=True) # Save DataFrame locally
    time.sleep(60) # Call function every 60 seconds
    time_duration += 1 ## Increment query duration by 1 mins at the end of every function call    
    