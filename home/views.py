from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pmdarima as pm
from pmdarima import model_selection
import datetime
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
showPredictions = False

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
    global showPredictions

    #handling button requests addSector-removeSector
    if (request.GET.get('addSector') != None):
        if (counterSector != 4):
            counterSector = counterSector + 1
            counterSectorArray.append(counterSector)
    if (request.GET.get('removeSector') != None):
        if (counterSector != 1):
            counterSector = counterSector - 1
            counterSectorArray.pop()
    if (request.GET.get('makePredictions') != None):
        showPredictions = True

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

    def makePredictions(sectorsData):
        #filtering data
        dates = sectorsData['years']
        futureStepsN = 10
        forecastDates = []
        lastDate = dates[-1]

        for i in range(futureStepsN):
            lastDate = lastDate + datetime.timedelta(days=91)
            forecastDates.append(lastDate)
        
        forecastDates = pd.to_datetime(forecastDates)
        sectorsData['years'] = sectorsData['years'].append(forecastDates)
        
        for i in counterSectorArray:
            sectorName = 'Sector ' + str(i)
            values = sectorsData[sectorName]

            #clip1
            # print(vals)
            # minVal = min(vals)
            # maxval = max(vals)
            # meanVals = statistics.mean(vals)
            # sdVals = statistics.stdev(vals)
            # normVals = (vals-meanVals)/(sdVals)

            #creating data frame
            data = pd.DataFrame(
                {'dates': dates,
                'values': values
                })

            data.set_index('dates', inplace=True)

            #splitting into train_test data
            #train, test = model_selection.train_test_split(data, train_size=14)
            train = data

            #clip2
            # training_data_diff1 = training_data.diff().fillna(training_data)
            # training_data_diff2 = training_data_diff1.diff().fillna(training_data)
            #comparing differencing plots
            # pyplot.plot(training_data, 'b')
            # pyplot.plot(training_data_diff1, 'r')
            # pyplot.plot(training_data_diff2, 'g')
            # pyplot.show()

            #analyzing prediction plots
            # plot_acf(training_data_diff2)
            # pyplot.show()
            # plot_pacf(training_data_diff2)
            # pyplot.show()

            arima = pm.auto_arima(train, seasonal=True, m=4, error_action='ignore', trace=True,
                                suppress_warnings=True, maxiter=10)
            
            forecastValues = arima.predict(futureStepsN)
            
            forecast_data = pd.Series(forecastValues, index = forecastDates) 

            #clip3
            # forecastDates = []
            # lastDate = dates[-1]

            # for i in range(futureStepsN):
            #     lastDate = lastDate + datetime.timedelta(days=365)
            #     forecastDates.append(lastDate)

            # forecast_data = pd.DataFrame(
            #     {'datetime': forecastDates,
            #      'values': forecastValues
            #     })
            # forecast_data.set_index('datetime', inplace=True)
            # training_data.values = vals

            # pyplot.plot(training_data, 'b')
            # pyplot.plot(forecast_data, 'g')
            # pyplot.show()

            sectorsData[sectorName] = sectorsData[sectorName].append(forecast_data)

        return sectorsData

    def drawChart(chartType):
        x = pd.to_datetime(timeFrame_column_names)
        data = {'years': x}

        for i in counterSectorArray:
            sectorName = 'Sector ' + str(i)
            y = selected_data[i-1].iloc[0]
            y.index = x
            data[sectorName] = y

        if (showPredictions):
            data = makePredictions(data)

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

    

            
