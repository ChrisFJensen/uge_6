from etl_connector import connector
from etl_crud import CRUD
import load_api_data
import load_data_from_csv

# Create class that contains all functions needed to load to database
class load_to_database():
    def __init__(self, connector: connector):
        self.connector = connector
        self.crud = CRUD(self.connector)
        self.data = None
    
    def read_data_from_source(self,table_name: str, filepath = None):
        if table_name in ["orders","order_items","customers"]:
            self.data = load_api_data.api_data(table_name)
            return self.data
        else:
            if filepath == None:
                self.data = load_data_from_csv.load_data_csv_path(filepath)
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

# Function that loads data to db
def load_data_to_db(tables: list, connector:connector):
    loader = load_to_database(connector)
    for table in tables:
        loader.load(table)
    return None