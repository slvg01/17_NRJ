import pandas as pd
import requests
import json
import time
from datetime import datetime, timedelta
import pyodbc

URL = "https://opendata.elia.be/api/explore/v2.1/catalog/datasets/ods177/records"
start_datetime = datetime(2025, 1, 1, 0, 0)
end_datetime = datetime(2025, 1, 3, 23, 59)

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
            params = {
                "limit": limit,
                "offset": offset,
                "refine": f'datetime:"{current_date.strftime("%Y-%m-%d")}"'  # Filter by date
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
    
    print(f"Number of lines: {len(df)}")
    print(df.head())  # Display first few rows for inspection
    
    return df

# Call the function with the refined URL for March 2025
df = extract_data_by_day(URL, start_datetime, end_datetime)
df.to_csv('data.csv', index=False)  # Save the data to a CSV file
