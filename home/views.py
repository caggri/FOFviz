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
selectedSector3 = None
selectedSector4 = None
counterSector = 1
counterSectorArray = [counterSector]
plotTypes = ['scatter', 'dotPlot', 'lineChart', 'groupedBarChart']

def home(request):
    global selectedSector
    global selectedSector2
    global selectedSector3
    global selectedSector4
    global counterSector

    #handling button requests addSector-removeSector
    if (request.GET.get('addSector') != None):
        if (counterSector != 4):
            counterSector = counterSector + 1
            counterSectorArray.append(counterSector)
    if (request.GET.get('removeSector') != None):
        if (counterSector != 1):
            counterSector = counterSector - 1
            counterSectorArray.pop()

    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'EVDSdata.xlsx')
    readFromDB()
    timeFrame_column_names = a.columns[a.columns.str.startswith('20')]
    sectors =  a[a.columns[1]]
    
    if 1 in counterSectorArray:
        selectedSector = sectors[1]
        
        if (request.GET.get('sectors') != None):
            selectedSector = request.GET.get('sectors')

        selected_data = a[a['Entry'] == selectedSector]
        selected_data.drop(selected_data.columns[[0, 1]], axis=1, inplace=True)

    if 2 in counterSectorArray:
        selectedSector2 = sectors[2]
        
        if (request.GET.get('sectors2') != None):
            selectedSector2 = request.GET.get('sectors2')

        selected_data_2 = a[a['Entry'] == selectedSector2]
        selected_data_2.drop(selected_data_2.columns[[0, 1]], axis=1, inplace=True)

    if 3 in counterSectorArray:
        selectedSector3 = sectors[3]
        
        if (request.GET.get('sectors3') != None):
            selectedSector3 = request.GET.get('sectors3')

        selected_data_3 = a[a['Entry'] == selectedSector3]
        selected_data_3.drop(selected_data_3.columns[[0, 1]], axis=1, inplace=True)

    if 4 in counterSectorArray:
        selectedSector4 = sectors[4]
        
        if (request.GET.get('sectors4') != None):
            selectedSector4 = request.GET.get('sectors4')

        selected_data_4 = a[a['Entry'] == selectedSector4]
        selected_data_4.drop(selected_data_4.columns[[0, 1]], axis=1, inplace=True)

    # def scatter():
    #     x1 = timeFrame_column_names
    #     y1 = selected_data.iloc[0]
    #
    #     trace = go.Scatter(
    #         x=x1,
    #         y=y1
    #     )
    #     layout = dict(
    #         title='Scatter Plot',
    #         xaxis=dict(range=[min(x1), max(x1)]),
    #         yaxis=dict(range=[min(y1), max(y1)])
    #     )
    #     fig = go.Figure(data=[trace], layout=layout)
    #     x2 = timeFrame_column_names
    #     y2 = selected_data_2.iloc[0]
    #
    #     trace = go.Scatter(
    #         x=x1,
    #         y=y1,
    #         name="Sector 1"
    #     )
    #
    #     trace2= go.Scatter(
    #         x=x2,
    #         y=y2,
    #         name="Sector 2"
    #     )
    #     layout = dict(
    #         title='Scatter Plot',
    #         xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
    #         yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
    #     )
    #     fig = go.Figure(data=[trace, trace2], layout=layout)
    #     plot_div = plot(fig, output_type='div', include_plotlyjs = False)
    #     return plot_div

    def dotPlot():
        x1 = timeFrame_column_names
        y1 = selected_data.iloc[0]

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
            y2 = selected_data_2.iloc[0]

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
        x1 = timeFrame_column_names
        y1 = selected_data.iloc[0]

        trace = go.Line(
            x=x1,
            y=y1
        )

        layout = dict(
            title='Line Chart Plot',
            xaxis=dict(range=[x1, x1]),
            yaxis=dict(range=[y1, y1])
        )

        fig = go.Figure(data=[trace], layout=layout)

        if 2 in counterSectorArray:
            x2 = timeFrame_column_names
            y2 = selected_data_2.iloc[0]

            trace = go.Line(
                x=x1,
                y=y1,
                name="Sector 1"
            )

            trace2 = go.Line(
                x=x2,
                y=y2,
                name="Sector 2"
            )

            layout = dict(
                title='Line Chart Plot',
                xaxis=dict(range=[min(min(x1),min(x2)), max(max(x1),max(x2))]),
                yaxis=dict(range=[min(min(y1),min(y2)), max(max(y1),max(y2))])
            )

            fig = go.Figure(data=[trace, trace2], layout=layout)

        if 3 in counterSectorArray:
            x3 = timeFrame_column_names
            y3 = selected_data_3.iloc[0]

            trace3 = go.Line(
                x=x3,
                y=y3,
                name="Sector 3"
            )

            layout = dict(
                title='Line Chart Plot',
                xaxis=dict(range=[min(min(x1),min(x2),min(x3)), max(max(x1),max(x2),max(x3))]),
                yaxis=dict(range=[min(min(y1),min(y2),min(y3)), max(max(y1),max(y2),max(y3))])
            )

            fig = go.Figure(data=[trace, trace2, trace3], layout=layout)

        if 4 in counterSectorArray:
            x4 = timeFrame_column_names
            y4 = selected_data_4.iloc[0]

            trace4 = go.Line(
                x=x4,
                y=y4,
                name="Sector 4"
            )

            layout = dict(
                title='Line Chart Plot',
                xaxis=dict(range=[min(min(x1),min(x2),min(x3),min(x4)), max(max(x1),max(x2),max(x3),max(x4))]),
                yaxis=dict(range=[min(min(y1),min(y2),min(y3),min(y4)), max(max(y1),max(y2),max(y3),max(y4))])
            )

            fig = go.Figure(data=[trace, trace2, trace3, trace4], layout=layout)

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    def groupedBarChart():
        x1 = timeFrame_column_names
        y1 = selected_data.iloc[0]

        trace = go.Bar(
            x=x1,
            y=y1
        )

        layout = dict(
            title='Grouped Bar Plot',
            xaxis=dict(range=[x1, x1]),
            yaxis=dict(range=[y1, y1])
        )

        fig = go.Figure(data=[trace], layout=layout)


        if 2 in counterSectorArray:
            x2 = timeFrame_column_names
            y2 = selected_data_2.iloc[0]

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
            y3 = selected_data_3.iloc[0]

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
            y4 = selected_data_4.iloc[0]

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
        'plot': groupedBarChart(),
        'sectors': sectors,
        'selectedSector': selectedSector,
        'selectedSector2': selectedSector2,
        'selectedSector3': selectedSector3,
        'selectedSector4': selectedSector4,
        'counterSectorArray': counterSectorArray
    }

    return render(request, 'home/dashboard.html', context)
