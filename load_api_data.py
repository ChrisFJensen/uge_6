import requests
import pandas as pd
import os

def api_data(name: str):
    #Checks for which API i am getting data from
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
    #Converts to pandas df because i like working in them
    df = pd.DataFrame.from_dict(response.json())
    return df


#Writes pandas DF to CSV
def to_csv(name: str, data: pd.DataFrame):
    base_dir = os.path.join("Data opsætning" ,"Data CSV")
    write_to = os.path.join(base_dir,f"{name}.csv")
    data.to_csv(write_to, index=False)



