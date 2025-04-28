import pandas as pd
import requests
import json
import time
from datetime import datetime, timedelta
import pyodbc


#dataset_id = "ods033"  # old dataset generated 
dataset_id = "ods177"  #new dataset generated power
#dataset_id = "ods036"  # old dataset installed power
#dataset_id = "ods179"  # new dataset installed power



URL = f'https://opendata.elia.be/api/explore/v2.1/catalog/datasets/{dataset_id}/records'
if dataset_id == "ods033" or dataset_id == "ods036":
    start_datetime = datetime(2018, 1, 1 , 0, 0)
    end_datetime = datetime(2023, 1, 1, 23, 59)
else:
    start_datetime = datetime(2025, 2, 1 , 0, 0)
    end_datetime = datetime(2025, 3, 31, 23, 59)

# Configuration de la connexion à SQL Server
server = r'localhost\SQLEXPRESS'
database = 'nrj_data'



def extract_data_by_day(URL, start_datetime, end_datetime):
    # Parameters for filtering and pagination
    limit = 100  # Max number of records per request
    all_records = []  # List to store all data
    retry_attempts = 3  # Maximum number of retries
    backoff_time = 10  # Initial backoff time in seconds
    
    # Loop through each day between start_datetime and end_datetime
    current_date = start_datetime
    while current_date <= end_datetime:
        offset = 0
        page = 1  # Reset page for each new day
        
        while True:
            # Construct API request with the specific day filter
            if dataset_id == "ods033" or dataset_id == "ods177" :
                params = {
                "limit": limit,
                "offset": offset,
                "refine": f'datetime:"{current_date.strftime("%Y-%m-%d")}"'  # Filter by date
                }
            else: 
                params = {
                "limit": limit,
                "offset": offset,
                "refine": f'date:"{current_date.strftime("%Y-%m-%d")}"'  # Filter by date
                }  
            
            response = requests.get(URL, params=params)
            
            if response.status_code == 429:  # Rate-limit error (too many requests)
                if retry_attempts > 0:
                    print(f"Rate limit hit. Retrying in {backoff_time} seconds...")
                    time.sleep(backoff_time)
                    backoff_time *= 2  # Exponential backoff
                    retry_attempts -= 1
                    continue
                else:
                    print("Max retry attempts reached. Stopping.")
                    break
            
            elif response.status_code != 200:
                print(f"Failed to get data, status code: {response.status_code}")
                print("Response Body:", response.text)
                break
            
            else:
                print(f"Successfully got data for date: {current_date.strftime('%Y-%m-%d')}, page {page}")
                data = response.json()
                records = data.get('results', [])
                
                if not records:
                    break  # Exit loop when no more data
                
                all_records.extend(records)  # Store retrieved data
                page += 1
                offset += limit  # Move to the next page
        
        # Move to the next day
        current_date += timedelta(days=1)
    
    # Normalize the JSON response into a flat table (DataFrame)
    df = pd.json_normalize(all_records)
    if dataset_id == "ods033" or dataset_id == "ods177":
        df['datetime'] = pd.to_datetime(df['datetime']).dt.tz_localize(None)
   
    if dataset_id == "ods033" :
        df.to_pickle("prod_old.pkl")
    elif dataset_id == "ods177":
        df.to_pickle("prod_new.pkl")
    elif dataset_id == "ods036":  
        df.to_pickle("installed_power_old.pkl")
    elif dataset_id == "ods179":
        df.to_pickle("installed_power_new.pkl")
    
    print(f"Number of lines: {len(df)}")
    print(df.dtypes)
    print(df.head(1))  # Display first few rows for inspection
    print(df.tail(1))  # Display first few rows for inspection
    
    df.to_csv('data.csv', index=False)  # Save the data to a CSV file
    
    return df

#initialize the connexion to the local server
def create_connection ():
    try:
        conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};'
                              f'SERVER={server};'        # Using the variable for server
                              f'DATABASE={database};'    # Using the variable for database
                              'Trusted_Connection=yes')  # Use Windows Authentication
        print("Connection successful!")
        return conn  # Return the connection object
    except Exception as e:
        print(f"Failed to connect: {e}")



# Fonction pour charger les données dans la table SQL Server
def load_data_to_sql(df, table_name):

    conn = create_connection()
    cursor = conn.cursor()
    columns = ", ".join(df.columns)

    for _, row in df.iterrows():
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({', '.join(['?' for _ in df.columns])})"
        cursor.execute(insert_query, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Les données ont été chargées avec succès dans la table {table_name}.")

# Appeler la fonction pour extraire les données
df = extract_data_by_day(URL, start_datetime, end_datetime)


# Charger les données dans SQL Server
if dataset_id == "ods033":
    load_data_to_sql(df, 'prod_old')
elif dataset_id == "ods177":
    load_data_to_sql(df, 'prod_new')
elif dataset_id == "ods036":
    load_data_to_sql(df, 'installed_power_old')
elif dataset_id == "ods179":
    load_data_to_sql(df, 'installed_power_new')
    



