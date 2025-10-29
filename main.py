from etl_connector import connector
from read_sources import extractor
from transform_data import transformer
from loader import loader
import os


# Order of load order of tables
table_order = ["brands","categories","products","customers","stores","staffs","stocks","orders","order_items"]


# Create connection
database = connector()
database.connect()
database.is_open()
# Create/Choose desired DB
database.create_db("uge6_database")
#Initialise tables based on a scheme
database.initialise_tables("SQL_tables.sql")

#Start our classes
extract = extractor()
transform = transformer(database)
load = loader(database)

#ETL Process

def etl_process(table_name: str):
    if table_name in ["orders","order_items","customers"]:
        data = extract.extract_api(table_name)
    else:
        file_path = os.path.join("Data opsætning","Data CSV",f"{table_name}.csv")
        data = extract.extract_csv(file_path)
    data_t = transform.transform(data,table_name)
    load.load_data(data_t, table_name)
    return None

test_data = extract.extract_api("orders")
load.load_data(test_data,"orders")

for table_name in table_order:
    etl_process(table_name)