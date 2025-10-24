import mysql.connector

class connector:
    # Define some parameters for the class
    def __init__(self,user="user", password="password", host="localhost",database = None):
        self.host = host           #Used for establishing connection
        self.user = user           #Used for establishing connection
        self.passwd = password     #Used for establishing connection
        self.database = database   #Used to check database
        self.conn = None           #Used to check if connection was made and store it
        self.cursor = None         #Used to do cursor things later
        self.table_list = None     #Used to check if table exists in DB
    
    #Create a method to open connection to sql server
    def connect(self):
        # Adds try if invalid arguments is given
        try:
            self.conn = mysql.connector.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.database
            )
            print("Connection opened")
            self.cursor = self.conn.cursor()
            self.update_table_list()
        #If connection fails, prints that it failed
        except mysql.connector.Error:
            print("Connection failed")
            pass
    
    #Creates a method to close the connection to the server
    def close(self):
        #Tries to check if connection is open
        try:
            #Checks if connection is open, if open closes the connection and prints action
            if self.conn.is_connected():
                self.conn.close()
                print("Connection closed")
            else:
                print("Connection already closed")
        #If the connection was never made, then the conn object would be none.
        except AttributeError:
            if self.conn:
                pass
            else:
                print("Connection not created")
    
    #Adds a method that checks if connection is currently open
    def is_open(self):
        if self.conn and self.conn.is_connected():
            return True
        else:
            return False
    
    #Create method to show database
    def show_dbs(self):
        try:
            self.cursor.execute("SHOW DATABASES")
            db_list = []
            for db in self.cursor:
                db_list.append(db[0])
            return db_list
        except:
            pass

    #Method to create and activate a new DB
    def create_db(self, db_name: str):
        try:
            self.cursor.execute(f"CREATE DATABASE {db_name}")
            self.cursor.execute(f"USE {db_name}")
            self.cursor.execute("SELECT DATABASE()")
            for db in self.cursor:
                self.database = db[0]
            self.update_table_list()
        except mysql.connector.DatabaseError:
            print(f"DB already exists, makes {db_name} active instead")
            self.choose_db(db_name)

    #Create Method to select database
    def choose_db(self, db_name: str):
        try:
            self.cursor.execute(f"USE {db_name}")
            self.cursor.execute("SELECT DATABASE()")
            for db in self.cursor:
                self.database = db[0]
            self.update_table_list()
        except mysql.connector.ProgrammingError:
            pass
    
    #Create method to get current db name
    def current_db(self):
            self.cursor.execute("SELECT DATABASE()")
            for db in self.cursor:
                print(db[0])

    #Create Method to drop database
    def drop_db_current(self):
        try:
            self.cursor.execute(f"DROP DATABASE {self.database}")
        except:
            pass

    #Method to get existing tables in the chosen db
    def update_table_list(self):
        if self.database==None:
            self.table_list = None
        else:
            try:
                self.cursor.execute("SHOW TABLES")
                table_list = []
                for table_name in self.cursor:
                    table_list.append(table_name[0])
                self.table_list = table_list
            except:
                pass

    #Create Table
    def create_table(self, query: str):
        try:
            self.cursor.execute(query)
            self.update_table_list()
        except mysql.connector.ProgrammingError as e:
            print(e)
            return None

    #Drop Table
    def drop_table(self, table_name: str):
        try:
            self.cursor.execute(f"""DROP TABLE {table_name}""")
            self.update_table_list()
        except mysql.connector.ProgrammingError as e:
            print(e)
            return None
    
    #Delete all table data
    def del_table_data(self, table_name:str):
        try:
            self.cursor.execute(f"""TRUNCATE TABLE {table_name}""")
        except mysql.connector.ProgrammingError as e:
            print(e)
            return None

    #Show tables
    def show_tables(self):
        self.update_table_list()
        print(self.table_list)

if __name__ == "__main__":
    test = connector("user","password")
    test.connect()
    test.show_dbs()
    test.close()
    test.is_open()
    test.create_db("gfg")
    test.choose_db("uge6_database")
    test.show_dbs()
    test.update_table_list()
    test.show_tables()
    test.current_db()
    test.drop_db_current()
    print(test.database)
    print(test.cursor)
    for db in test.cursor:
        print(db[0])

    if test.conn:
        print(test.conn)
    else:
        print("closed")
