import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from sqlalchemy import create_engine
import os
import datetime

def handle_uploaded_file(f, data_type): 
    print( "Data typle:", data_type) 
    if data_type == "fof":
        file_name = "fof.xlsx"
        table_name="records"
    
    if data_type == "annually":
        file_name = "annual.xlsx"
        table_name="annually"
    
    if data_type == "monthly":
        file_name = "monthly.xlsx"
        table_name = "monthly"

    print("File name:", file_name)
    path_str = 'upload/data/'+file_name
    print("Str of path:", path_str)
    
    with open(path_str, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)


    date = datetime.datetime.now()
    file_str = date.strftime("%Y%m%d"+file_name)

    df = pd.read_excel('upload/data/' +file_name, sheet_name='EVDS', index=False)
    new_df = df.iloc[:, 1:] ##It takes everything except row numbers

    dataFrame = new_df

    #print(new_df.head())

    sqlEngine = create_engine('postgresql+psycopg2://postgres:password@127.0.0.1/data')
    #sqlEngine = create_engine('postgresql+psycopg2://postgres:CT1SEr.FtW@database-1.cczlh6s4kbhf.us-east-1.rds.amazonaws.com/data')

    dbConnection = sqlEngine.connect()

    try:

        frame = dataFrame.to_sql(table_name, dbConnection, if_exists='replace')

    except ValueError as vx:

        print(vx)

    except Exception as ex:   

        print(ex)

    else:

        print("Table %s created successfully." % table_name) 

    finally:
        dbConnection.close()
        print("--------------------------")
        print(file_name)
        os.rename('upload/data/'+file_name,'upload/data/'+file_str)



        # with open('upload/static/'+file_name, 'r') as destination:
        #     print(destination.read())  