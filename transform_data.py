import mysql.connector
import pandas as pd
import numpy as np
from etl_connector import connector
from read_sources import extractor


def get_store_id(connector: connector):
    # Get a list of current stores and their id's from the database
    try:
        read_data_query = f"""SELECT name,street,store_id FROM stores"""
        connector.cursor.execute(read_data_query)
        store_id_df = pd.DataFrame(connector.cursor.fetchall(), columns=["store_name","street","store_id"])
        return store_id_df
    except mysql.connector.ProgrammingError as e:
        print(e)
        return None

# Preps staffs data as specified in table_choices.txt
def prep_staffs_data(staff_df: pd.DataFrame, store_id_df: pd.DataFrame):
    # Adds the store id's to staff
    new_staff_df = staff_df.merge(store_id_df,on=["store_name","street"], how="left")
    #Removes store_name and street variables from staff dataframe
    new_staff_df = new_staff_df.drop(columns=["store_name","street"])
    new_staff_df["staff_id"] = None
    return new_staff_df.replace(np.nan,None)

# Preps stores data as specified
def prep_stores_data(stores_df: pd.DataFrame):
    data_df = stores_df
    data_df["store_id"] = None
    return data_df.replace(np.nan,None)

# Prep order_items table specified in table_choices
def prep_order_items_data(order_items_df: pd.DataFrame):
    data_df = order_items_df
    data_df = data_df.drop(columns="list_price")
    return data_df.replace(np.nan,None)

# Get staff_id from database
def get_staff_id(connector: connector):
    try:
        read_data_query = f"""SELECT name,staff_id,store_id FROM staffs"""
        connector.cursor.execute(read_data_query)
        staff_id_df = pd.DataFrame(connector.cursor.fetchall(), columns=["staff_name","staff_id", "store_id"])
        return staff_id_df
    except mysql.connector.ProgrammingError as e:
        print(e)
        return None

def get_store_id_orders(connector: connector):
    # Get a list of current stores and their id's from the database
    try:
        read_data_query = f"""SELECT name,store_id FROM stores"""
        connector.cursor.execute(read_data_query)
        store_id_df = pd.DataFrame(connector.cursor.fetchall(), columns=["store","store_id"])
        return store_id_df
    except mysql.connector.ProgrammingError as e:
        print(e)
        return None

# Prepare orders_df as specified in table_choices
def prep_orders_data(orders_df: pd.DataFrame, staff_id_df: pd.DataFrame, store_id_df: pd.DataFrame):
    # First adds the store_id
    new_orders_df = orders_df.merge(store_id_df,on=["store"], how="left")
    # adds staff_id
    new_orders_df = new_orders_df.merge(staff_id_df,on=["staff_name","store_id"], how="left")
    # remove extra columns
    new_orders_df = new_orders_df.drop(columns=["staff_name","store"])
    #Fix date_time format to SQL server
    date_columns = ["order_date","required_date","shipped_date"]
    new_orders_df[date_columns] = new_orders_df[date_columns].apply(pd.to_datetime, dayfirst=True, errors="coerce")
    #Change order of store_id and staff_id
    New_new_orders_df = new_orders_df.drop(columns=["store_id"])
    New_new_orders_df["store_id"] = new_orders_df["store_id"]
    return New_new_orders_df.replace(np.nan, None)

def prep_stocks_data(stocks_df: pd.DataFrame, store_id_df: pd.DataFrame):
    new_stocks_df = store_id_df.merge(stocks_df,on=["store_name"], how="left")
    new_stocks_df = new_stocks_df.drop(columns=["store_name","street"])
    return new_stocks_df.replace(np.nan, None)

def prep_data(data: pd.DataFrame, table_name: str, connector: connector):
    if table_name in ["brands","categories","customers","products"]:
        data.replace(np.nan,None)
        return data
    else:
        match table_name:
            case "staffs":
                store_ids = get_store_id(connector)
                return prep_staffs_data(data,store_ids)
            case "orders":
                store_ids = get_store_id_orders(connector)
                staff_ids = get_staff_id(connector)
                return prep_orders_data(data,staff_ids,store_ids)
            case "order_items":
                return prep_order_items_data(data)
            case "stores":
                return prep_stores_data(data)
            case "stocks":
                store_ids = get_store_id(connector)
                return prep_stocks_data(data,store_ids)
            case _:
                return None
            
class transformer():
    def __init__(self, connector:connector):
        self.connector = connector
    
    def transform(self, data: pd.DataFrame, table_name: str):
        return prep_data(data, table_name,self.connector)