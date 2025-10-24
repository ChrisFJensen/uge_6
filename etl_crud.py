import pandas as pd
import mysql.connector
from etl_connector import connector
import numpy as np
import prep_data

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
    except mysql.connector.ProgrammingError as e:
        print(f"Procedure failed because {e}")
        pass

def read_table(table_name:str, columns: list, connect: connector):
    try:
        Read_all_query= f"""SELECT * FROM {table_name}"""
        connect.cursor.execute(Read_all_query)
        sql_data = pd.DataFrame(connect.cursor.fetchall(), columns=columns)
        return sql_data
    except:
        pass

def update_table(table_name:str, condition:str, to_replace: str, connect: connector):
    try:
        update_query = f"""UPDATE {table_name}
        SET {to_replace}
        WHERE {condition};"""
        connect.cursor.execute(update_query)
        connect.cursor.execute("COMMIT;")
    except:
        pass

def delete_from_table(table_name: str, condition: str, connect:connector):
    try:
        delete_query = f""" DELETE FROM {table_name} WHERE {condition};"""
        connect.cursor.execute(delete_query)
        connect.cursor.execute("COMMIT")
    except:
        pass

def replace_table(table_name: str, connect:connector):
    pass

class CRUD():
    def __init__(self, connector: connector):
        self.connector = connector
        self.data = None
        self.table = None
        self.table_columns = None
    
    def choose_table(self, table_name: str):
        #Checks if a table exists in the database
        if table_name in self.connector.table_list:
            self.table = table_name
            self.table_columns = get_column_names(self.table,self.connector)
        else:
            self.table = None

    def prep_data(self, data: pd.DataFrame):
        self.data = prep_data.prep_data(data, self.table, self.connector)
        pass

    def write_to_table(self, data: pd.DataFrame, table_name: str):
        self.choose_table(table_name)
        if self.table == None:
            print("Non valid table given exiting")
            return None
        else:
            self.prep_data(data)
            write_to_table(self.table, self.data, self.connector)
            self.table=None

    def read_table(self,table_name:str):
        self.choose_table(table_name)
        if self.table == None:
            print("Table doesn't exists, exiting")
            return None
        else:
            self.data = read_table(self.table,self.table_columns, self.connector)
            return None
        


if __name__=="__main__":
    pass