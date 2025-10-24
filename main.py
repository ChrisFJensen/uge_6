import load_api_data
from etl_connector import connector
import SQL_tables
import load_data_from_csv
import etl_crud
import prep_data
import pandas as pd

class load_to_database():
    def __init__(self, connector: connector):
        self.connector = connector
        self.crud = etl_crud.CRUD(self.connector)
        self.data = None
    
    def read_data_from_source(self,table_name: str):
        if table_name in ["orders","order_items","customers"]:
            self.data = load_api_data.api_data(table_name)
            return self.data
        else:
            self.data = load_data_from_csv.load_data_csv(table_name)
            return self.data
    
    def load(self, table_name: str):
        self.read_data_from_source(table_name)
        self.crud.write_to_table(self.data, table_name)
    
    def read(self, table_name: str):
        self.crud.read_table(table_name)
        print(self.crud.data)

# Order of load order of tables
table_order = ["brands","categories","products","customers","stores","staffs","stocks","orders","order_items"]

def load_data_to_db(tables: list, connector:connector):
    loader = load_to_database(connector)
    for table in tables:
        loader.load(table)
    return None

if __name__ == "__main__":

    # Create connection and database
    database = connector()
    database.connect()
    database.is_open()
    database.create_db("uge6_database")
    database.drop_db_current()
    database.show_tables()


    load_data_to_db(table_order, database)
    # Create our loader object
    loader = load_to_database(database)
    database.close()

for table in SQL_tables.table_list:
    database.create_table(table)

for table in reversed(table_order):
    database.del_table_data(table)

for table in table_order:
    loader.load(table)

for table in table_order:
    print(loader.read(table))

loader.read_data_from_source("stocks")

stock_test = loader.data
print(prep_data.prep_data(stock_test,"stocks", database))
