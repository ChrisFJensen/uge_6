import pandas as pd
import mysql.connector
from etl_connector import connector
import numpy as np
from transform_data import transformer

def get_column_names(table_name: str, connect: connector):
    try:
        #Executes code to get describtion of table
        connect.cursor.execute(f"""DESCRIBE {table_name}""")
        column_list = []
        #Column name is the first value in each row, so only the names to a list
        for row in connect.cursor.fetchall():
            column_list.append(row[0])
        #Prints the list
        return column_list
    except:
        pass

def fix_column_list(column_list: list):
    try:
        #Changes list from get_column_names to work in a SQL query
        column_names = ",".join(column_list)
        return "("+column_names+")"
    except:
        pass

def write_to_table(table_name: str, data: pd.DataFrame, connect: connector):
    match table_name:
        case "brands":
            sql_command_insert = f"""INSERT INTO brands (brand_id,brand_name) VALUES (%s,%s)"""
        case "categories":
            sql_command_insert = f"""INSERT INTO categories (category_id,category_name) VALUES (%s,%s)"""
        case "customers":
            sql_command_insert = f"""INSERT INTO customers (
            city,customer_id,email,first_name,last_name,phone,state,street,zip_code)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        case "order_items":
            sql_command_insert = f"""INSERT INTO order_items (
            discount,item_id,order_id,product_id,quantity)
            VALUES (%s,%s,%s,%s,%s)"""
        case "orders":
            sql_command_insert = f"""INSERT INTO orders (
            customer_id,order_date,order_id,order_status,required_date,shipped_date, staff_id, store_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        case "products":
            sql_command_insert = f"""INSERT INTO products (
            product_id, product_name, brand_id, category_id, model_year, list_price)
            VALUES (%s,%s,%s,%s,%s,%s)"""
        case "staffs":
            sql_command_insert = f"""INSERT INTO staffs (
            name,last_name,email,phone,active,manager_id,store_id,staff_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        case "stocks":
            sql_command_insert = f"""INSERT INTO stocks (
            store_id,product_id, quantity)
            VALUES (%s,%s,%s)"""
        case "stores":
            sql_command_insert = f"""INSERT INTO stores (
            name,phone,email,street,city,state,zip_code,store_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        connect.cursor.executemany(sql_command_insert,data.values.tolist())
        connect.cursor.execute("COMMIT")
        return True
    except mysql.connector.Error as e:
        print(f"Procedure failed because {e}")
        return False

class loader():
    def __init__(self, connector: connector):
        self.connector = connector
        self.table = None
        self.table_columns = None
    
    def choose_table(self, table_name: str):
        #Checks if a table exists in the database
        if table_name in self.connector.table_list:
            self.table = table_name
            self.table_columns = get_column_names(self.table,self.connector)
        else:
            self.table = None

    def load_data(self, data: pd.DataFrame, table_name: str):
        self.choose_table(table_name)
        if self.table == None:
            print("Non valid table given exiting")
        else:
            write_to_table(self.table, data, self.connector)
            self.table=None


        