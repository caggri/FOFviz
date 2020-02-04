from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import os.path
from sqlalchemy import create_engine


# Create your views here.

def readFromDB():
       # sqlEngine = create_engine('mysql+pymysql://newuser:CT1SEr.FtW@localhost:3306/import')
    table_name = "records" 
    sqlEngine = create_engine('postgresql+psycopg2://postgres:1234567890@localhost/data')
    dbConnection = sqlEngine.connect()
    global a 
    a = pd.read_sql_table(table_name, dbConnection)
    dbConnection.close()

selectedSector = None
selectedSector2 = None
def home(request):
    global selectedSector
    global selectedSector2
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'EVDSdata.xlsx')
    readFromDB()
    timeFrame_column_names = a.columns[a.columns.str.startswith('20')]
    sectors =  a[a.columns[1]]

       
    selectedSector = sectors[1]
    selectedSector2 = sectors[2]
    
    if (request.GET.get('sectors') != None):
        selectedSector = request.GET.get('sectors')
    
    if (request.GET.get('sectors2') != None):
        selectedSector2 = request.GET.get('sectors2')

    selected_data = a[a['Entry'] == selectedSector]
    selected_data_2 = a[a['Entry'] == selectedSector2]
    
    selected_data.drop(selected_data.columns[[0, 1]], axis=1, inplace=True)
    selected_data_2.drop(selected_data_2.columns[[0, 1]], axis=1, inplace=True)

    def scatter():
        x1 = timeFrame_column_names
        y1 = selected_data.iloc[0]

        x2 = timeFrame_column_names
        y2 = selected_data_2.iloc[0]

        trace = go.Scatter(
            x=x1,
            y=y1,
            name="Sector 1"
        )

        trace2= go.Scatter(
            x=x2,
            y=y2,
            name="Sector 2"
        )

        layout = dict(
            title='Line Plot',
            xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
            yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
        )
        fig = go.Figure(data=[trace, trace2], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs = False)
        return plot_div

    context = {
        'plot': scatter(),
        'sectors': sectors,
        'selectedSector': selectedSector,
        'selectedSector2': selectedSector2
    }

    return render(request, 'home/dashboard.html', context)
