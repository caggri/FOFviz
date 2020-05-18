import pandas as pd
from sqlalchemy import create_engine

class DataRetriever:
    
    def retrieveAllData():
        global fof_data
        global monthly #balance sheet
        global annually #balance sheet
        fof_data = DataRetriever.retrieve("records")
        monthly = DataRetriever.retrieve("monthly")
        annually = DataRetriever.retrieve("annually")

    def openConnection():
        sqlEngine = create_engine('postgresql+psycopg2://postgres:CT1SEr.FtW@database-1.cczlh6s4kbhf.us-east-1.rds.amazonaws.com/data')
        dbConnection = sqlEngine.connect()
        return dbConnection

    def retrieve(table_name):
        print(table_name)
        
        dbConnection = DataRetriever.openConnection()
        
        global all_data
        
        all_data = pd.read_sql_table(table_name, dbConnection)
        print(all_data)
        dbConnection.close()
        
        return all_data

    def retrieveFofData():
        return fof_data

    def retrieveMonthlyData():
        return monthly

    def retrieveAnnuallyData():
        return annually

    def pushString(tablename, serializedString, username, datasource):
        dbConnection = DataRetriever.openConnection()
        
        sqlStatement = "INSERT INTO "+ tablename + "(username, userdata, datasource) VALUES ('"+username+"', '"+ serializedString +"' , '" + datasource +"')"
        print(sqlStatement) 

        dbConnection.execute(sqlStatement)

        dbConnection.close()


    def pullString(tablename, username, datasource):
        dbConnection = DataRetriever.openConnection()
        
        sqlStatement = "SELECT userdata FROM " + tablename + " WHERE username='" + username +"' AND datasource='"+datasource+"';"
         
        print(sqlStatement) 

        rs = dbConnection.execute(sqlStatement).fetchall()

        dbConnection.close()

        return rs
