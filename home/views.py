from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
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
plotDictionary = {'Line Plot': 'line', 'Stacked Bar Chart' : 'bar', 'Grouped Bar Chart' : 'bar', 'Scatter Plot': 'scatter', 'Alluvial Diagram': 'parallel_categories', 'Area Graph': 'area', 'Density Contour': 'density_contour','Heat Map': 'density_heatmap'}


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

    def getParams(chartType):
        if (chartType=='Line Plot' or chartType=='Scatter Plot' or chartType=='Stacked Bar Chart' or chartType == 'Area Graph' or chartType == 'Density Contour'):
            params = {'x':'years', 'y':'value','color':'variable'}
        elif (chartType=='Alluvial Diagram'):
            params = {'color':'value', 'color_continuous_scale':px.colors.sequential.Inferno}
        elif (chartType == 'Heat Map'):
            params = {'x':'years', 'y':'value'}
        elif (chartType == 'Grouped Bar Chart'):
            params = {'x':'years', 'y':'value','color':'variable', 'barmode':'group'} 
        return params

    def drawChart(chartType):
        x = timeFrame_column_names
        data = {'years': x}

        for i in counterSectorArray:
            sectorName = 'Sector ' + str(i)
            y = selected_data[i-1].iloc[0]
            data[sectorName] = y

        df= (pd.DataFrame.from_dict(data,orient='index').transpose()).melt(id_vars="years")

        params = getParams(chartType)        

        fig = getattr(px, plotDictionary[chartType])(
                df,
                **params
            )

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)
        return plot_div

    if request.GET.get('plots') is None:
        getSelectedPlot = drawChart(list(plotDictionary.keys())[-1])
    else:
        getSelectedPlot = drawChart(request.GET.get('plots'))

    context = {
        'plot': getSelectedPlot,
        'sectors': sectors,
        'selectedSector1': selectedSectors[0],
        'selectedSector2': selectedSectors[1],
        'selectedSector3': selectedSectors[2],
        'selectedSector4': selectedSectors[3],
        'counterSectorArray': counterSectorArray,
        'plotTypes': plotDictionary.keys(),
        'selectedPlot': request.GET.get('plots')
    }

    return render(request, 'home/dashboard.html', context)

    

            
