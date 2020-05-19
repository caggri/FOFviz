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

    def pushToTable(userdata, username, datasource, requestType, usedGraphNames, description, graphName):
        dbConnection = DataRetriever.openConnection()
        description = description.replace("'", "''")
        if(requestType == "custom_request"):
            sqlStatement = "INSERT INTO user_custom_data(username, userdata, datasource) VALUES ('"+username+"', '"+ userdata +"' , '" + datasource +"');"
        elif(requestType == "important_request"):
            sqlStatement = "INSERT INTO important_graph_data(username, usedgraphnames, graphName, graphdatasource, description) VALUES ('"+username+"', '"+ usedGraphNames +"', '" + graphName +"', '"+ datasource +"', '"+ description+"');"
        
        print(sqlStatement) 

        dbConnection.execute(sqlStatement)

        dbConnection.close()


    def pullFromTable(username, datasource, requestType):
        dbConnection = DataRetriever.openConnection()
        
        if(requestType == "custom_request"):
            sqlStatement = "SELECT userdata FROM user_custom_data WHERE username='" + username +"' AND datasource='"+datasource+"';"
        elif(requestType == "important_request"):
            sqlStatement = "SELECT usedgraphnames, graphname, description FROM important_graph_data WHERE username='" + username +"' AND graphdatasource='"+datasource+"';"

        print(sqlStatement) 

        rs = dbConnection.execute(sqlStatement).fetchall()

        dbConnection.close()

        return rs
