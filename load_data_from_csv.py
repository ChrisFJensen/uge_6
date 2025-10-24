import os
import pandas as pd
import re

def get_file_list(target_dir: str):
    #Overvejer om at tilføje Regex til at søge ekslusivt for CSV filer
    file_list = os.listdir(target_dir)
    return file_list

#Load data from the Data CSV library
def load_data_csv(filename: str):
    file = os.path.join("Data opsætning","Data CSV",f"{filename}.csv")
    df = pd.read_csv(file)
    return df



