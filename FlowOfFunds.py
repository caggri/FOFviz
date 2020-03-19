import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
from sqlalchemy import create_engine
import os
import datetime

date = datetime.datetime.now()
file_str = date.strftime("%d_%m_%Y_%H:%M") + ".xlsx"

df = pd.read_excel('EVDSdata.xlsx', sheet_name='EVDS', index=False)
new_df = df.iloc[:, 1:] ##It takes everything except row numbers

table_name = "records"

dataFrame = new_df

#print(new_df.head())

#sqlEngine = create_engine('postgresql+psycopg2://postgres:1234567890@localhost/data')
   # sqlEngine = create_engine('mysql+pymysql://newuser:CT1SEr.FtW@localhost:3306/import')
sqlEngine = create_engine('postgresql+psycopg2://postgres:CT1SEr.FtW@database-1.cczlh6s4kbhf.us-east-1.rds.amazonaws.com/data')

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
    os.rename('EVDSdata.xlsx',file_str)

