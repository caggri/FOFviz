from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import os.path
from sqlalchemy import create_engine

# Create your views here.

# def readFromDB():
#        # sqlEngine = create_engine('mysql+pymysql://newuser:CT1SEr.FtW@localhost:3306/import')
#     table_name = "records" 
#     sqlEngine = create_engine('postgresql+psycopg2://postgres:1234567890@localhost/data')
#     dbConnection = sqlEngine.connect()
#     global a 
#     a = pd.read_sql_table(table_name, dbConnection)
#     dbConnection.close()


selectedSectors = [None,None,None,None]
selected_data = [None,None,None,None]
counterSector = 1
counterSectorArray = [counterSector]
plotTypes = ['scatter', 'dotPlot', 'lineChart', 'groupedBarChart']

#Keep read function here so it only executes it ones and keep one list with all the data, don't end it, make copies of it for further work
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, 'EVDSdata.xlsx')
#retriever = DataRetrieve.DataRetriever()
#all_data = retriever.retrieve()
a = pd.read_excel(path)

def home(request):
    global selectedSectors
    global counterSector
    global a

    #handling button requests addSector-removeSector
    if (request.GET.get('addSector') != None):
        if (counterSector != 4):
            counterSector = counterSector + 1
            counterSectorArray.append(counterSector)
    if (request.GET.get('removeSector') != None):
        if (counterSector != 1):
            counterSector = counterSector - 1
            counterSectorArray.pop()
    # readFromDB()
    timeFrame_column_names = a.columns[a.columns.str.startswith('20')]
    sectors =  a[a.columns[1]]
    
    for i in counterSectorArray:
        selectedSectors[i-1] = sectors[i]
        requestString = 'sectors' + str(i)
        if (request.GET.get(requestString) != None):
            selectedSectors[i-1] = request.GET.get(requestString)

        selected_data[i-1] = a[a['Entry'] == selectedSectors[i-1]]
        selected_data[i-1].drop(selected_data[i-1].columns[[0, 1]], axis=1, inplace=True)

    # def scatter():
    #     x1 = timeFrame_column_names
    #     y1 = selected_data[0].iloc[0]

    #     trace = go.Scatter(
    #         x=x1,
    #         y=y1
    #     )
    #     layout = dict(
    #         title='Line Plot',
    #         xaxis=dict(range=[min(x1), max(x1)]),
    #         yaxis=dict(range=[min(y1), max(y1)])
    #     )
    #     fig = go.Figure(data=[trace], layout=layout)
    #     x2 = timeFrame_column_names
    #     y2 = selected_data[1].iloc[0]

    #     trace = go.Scatter(
    #         x=x1,
    #         y=y1,
    #         name="Sector 1"
    #     )

    #     trace2= go.Scatter(
    #         x=x2,
    #         y=y2,
    #         name="Sector 2"
    #     )
    #     layout = dict(
    #         title='Line Plot',
    #         xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
    #         yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
    #     )
    #     fig = go.Figure(data=[trace, trace2], layout=layout)
    #     plot_div = plot(fig, output_type='div', include_plotlyjs = False)
    #     return plot_div

    def dotPlot():
        x1 = timeFrame_column_names
        y1 = selected_data[0].iloc[0]

        trace = go.Scatter(
            x=x1,
            y=y1,
            mode='markers'
        )

        layout = dict(
            title='Dot Plot',
            xaxis=dict(range=[x1, x1]),
            yaxis=dict(range=[y1, y1])
        )

        fig = go.Figure(data=[trace], layout=layout)

        if 2 in counterSectorArray:
            x2 = timeFrame_column_names
            y2 = selected_data[1].iloc[0]

            trace = go.Scatter(
                x=x1,
                y=y1,
                mode='markers',
                name="Sector 1"
            )

            trace2 = go.Scatter(
                x=x2,
                y=y2,
                mode='markers',
                name="Sector 2"
            )

            layout = dict(
                title='Dot Plot',
                xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
                yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
            )

            fig = go.Figure(data=[trace, trace2], layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
       
    def lineChart():
        allPlotDatas = []
        minimumsX = []
        maximumsX = []
        minimumsY = []
        maximumsY = []
        for i in counterSectorArray:
            x = timeFrame_column_names
            y = selected_data[i-1].iloc[0]
            minimumsX.append(min(x))
            maximumsX.append(max(x))
            minimumsY.append(min(y))
            maximumsY.append(max(y))

            trace = go.Line(
                x=x,
                y=y,
                name = "sector " + str(i)
            )

            allPlotDatas.append(trace)

        layout = dict(
            title='Line Chart Plot',
            xaxis=dict(range=[min(minimumsX), max(maximumsX)]),
            yaxis=dict(range=[min(minimumsY), max(maximumsY)])
        )

        fig = go.Figure(data=allPlotDatas, layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div
    
    def groupedBarChart():
        x1 = timeFrame_column_names
        y1 = selected_data[0].iloc[0]

        trace = go.Bar(
            x=x1,
            y=y1
        )

        layout = dict(
            title='Grouped Bar Plot',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )

        fig = go.Figure(data=[trace], layout=layout)

        if 2 in counterSectorArray:
            x2 = timeFrame_column_names
            y2 = selected_data[1].iloc[0]

            trace = go.Bar(
                x=x1,
                y=y1,
                name="Sector 1"
            )

            trace2 = go.Bar(
                x=x2,
                y=y2,
                name="Sector 2"
            )

            layout = dict(
                title='Grouped Bar Plot',
                xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
                yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
            )

            fig = go.Figure(data=[trace, trace2], layout=layout)
        
        if 3 in counterSectorArray:
            x3 = timeFrame_column_names
            y3 = selected_data[2].iloc[0]

            trace3 = go.Bar(
                x=x3,
                y=y3,
                name="Sector 3"
            )

            layout = dict(
                title='Grouped Bar Plot',
                xaxis=dict(range=[min(min(x1),min(x2),min(x3)), max(max(x1),max(x2),max(x3))]),
                yaxis=dict(range=[min(min(y1),min(y2),min(y3)), max(max(y1),max(y2),max(y3))])
            )

            fig = go.Figure(data=[trace, trace2, trace3], layout=layout)

        if 4 in counterSectorArray:
            x4 = timeFrame_column_names
            y4 = selected_data[3].iloc[0]

            trace4 = go.Bar(
                x=x4,
                y=y4,
                name="Sector 4"
            )

            layout = dict(
                title='Grouped Bar Plot',
                xaxis=dict(range=[min(min(x1),min(x2),min(x3),min(x4)), max(max(x1),max(x2),max(x3),max(x4))]),
                yaxis=dict(range=[min(min(y1),min(y2),min(y3),min(y4)), max(max(y1),max(y2),max(y3),max(y4))])
            )

            fig = go.Figure(data=[trace, trace2, trace3, trace4], layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    context = {
        'plot': lineChart(),
        'sectors': sectors,
        'selectedSector1': selectedSectors[0],
        'selectedSector2': selectedSectors[1],
        'selectedSector3': selectedSectors[2],
        'selectedSector4': selectedSectors[3],
        'counterSectorArray': counterSectorArray
    }

    return render(request, 'home/dashboard.html', context)
