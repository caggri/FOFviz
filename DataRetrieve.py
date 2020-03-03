import pandas as pd
from sqlalchemy import create_engine

class DataRetriever:
    def __init__(self, table_name):
        self.table_name = table_name

    def retrieve(self):
        table_name = self.table_name
        print(table_name)
        
        sqlEngine = create_engine('postgresql+psycopg2://postgres:CT1SEr.FtW@database-1.cczlh6s4kbhf.us-east-1.rds.amazonaws.com/data')
        dbConnection = sqlEngine.connect()
        global all_data
        
        all_data = pd.read_sql_table(table_name, dbConnection)
        print(all_data)
        dbConnection.close()
        #print(all_data)
        return all_data