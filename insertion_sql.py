import pandas as pd
import requests
#import pyodbc
import json


URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods177/records?limit=2&offset=0"
URL2 ="https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods177/records?limit=2&refine=datetime%3A%222025%22"

def extract_data (URL):
    response = requests.get(URL)
    if response.status_code != 200:
        print('Failed to get data:', response.status_code)
        return
    else:
        print('Successfully got data:', response.status_code)
        data = response.json()
        print(json.dumps(data, indent=2)) # pretty print
        records = data['results']
        df = pd.json_normalize(records)
        print (len(df))
        print(df)
        
        return df
    


extract_data(URL2)
