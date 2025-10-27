import load_api_data
from etl_connector import connector
import SQL_tables
import load_data_from_csv
import etl_crud
import prep_data
import pandas as pd
import classes


# Order of load order of tables
table_order = ["brands","categories","products","customers","stores","staffs","stocks","orders","order_items"]



if __name__ == "__main__":

    # Create connection and database
    database = connector()
    database.connect()
    database.is_open()
    database.create_db("uge6_database")
    database.drop_db_current()
    database.show_tables()


    classes.load_data_to_db(table_order, database)
    # Create our loader object
    loader = classes.load_to_database(database)
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
