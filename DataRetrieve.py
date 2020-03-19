import pandas as pd
from sqlalchemy import create_engine

class DataRetriever:
    def retrieve(self):
    # def readFromDB():
    #    # sqlEngine = create_engine('mysql+pymysql://newuser:CT1SEr.FtW@localhost:3306/import')
        table_name = "records" 
        sqlEngine = create_engine('postgresql+psycopg2://postgres:CT1SEr.FtW@database-1.cczlh6s4kbhf.us-east-1.rds.amazonaws.com/data')
        dbConnection = sqlEngine.connect()
        global all_data
        all_data = pd.read_sql_table(table_name, dbConnection)
        dbConnection.close()
        print(all_data)
        return all_data

if __name__ == '__main__':
    data = DataRetriever()
    data.retrieve()