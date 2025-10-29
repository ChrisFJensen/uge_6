import requests
import pandas as pd
import os
from etl_connector import connector

def api_data(name: str, url = None):
    #Checks for which API i am getting data from
    if url == None:
        match name:
            case "orders":
                url = "https://etl-server.fly.dev/orders"
            case "order_items":
                url = "https://etl-server.fly.dev/order_items"
            case "customers":
                url = "https://etl-server.fly.dev/customers"
            case _:
                #If no valid API name was given
                print("Please enter a valid api identifier")
                return None
    #Gets response from server
    response = requests.get(url)
    #Checks if request was made succesfully
    if response.status_code == 200:
        #Converts to pandas df
        df = pd.DataFrame.from_dict(response.json())
        return df
    else:
        print("request unsuccessfull")
        return None

# Extract data from a CSV
def extract_data_csv_path(filepath: str):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError as e:
        print(e)
        return None
    
class extractor():
    def __init__(self):
        pass    

    def extract_csv(self, filename: str):
        return extract_data_csv_path(filename) 

    def extract_api(self, name: str, url=None):
        return api_data(name,url)

    def extract_sql(self):
        print("SQL implementation has not been implemented")
        return None

