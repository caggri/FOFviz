from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
import pmdarima as pm
from pmdarima import model_selection
import datetime
import pandas as pd
import os.path
import DataRetrieve
from sqlalchemy import create_engine
import operator
import wikipedia
from io import StringIO

#determine selection
selectedPreviousDataName = None
showPredictions = False
selectedDataName = None #the type of data sheet selected (balance sheet etc)
selectedSectors = [None,None,None,None] #the names of the 4 selected sectors
selected_data = [None,None,None,None] #the filtered values for the 4 selected sectors
selectedImportantGraph = None  
selectedPreviousImportantGraph = None
timeFrame_column_names = [] #all avaialble time-frames
sectors = [] #unfiltered data
selectedSectorsDefinitions = [None,None,None,None] #wikipedia summary for the selected sectors

#List Elements
dataNames = ['Flow of Funds', 'Balance of Payment (Monthly)', 'Balance of Payment (Annual)', 'Balance Sheet (Assets)', 'Balance Sheet (Liabilities)'] #available data sheets
predictionModes = ['Disable Forecast', 'Enable Forecast']
importantGraphs = {} #to map all important graph names with the retrieved data from the database
importantGraphDescriptions = {} #retrieved description for the graph from the database
counterSector = 1 #number of sectors selected for comparison
counterSectorArray = [counterSector] #to allow for easy looping
plotDictionary = {'Line Plot': 'line', 'Stacked Bar Chart' : 'bar', 'Grouped Bar Chart' : 'bar', 
'Scatter Plot': 'scatter', 'Alluvial Diagram': 'parallel_categories', 'Area Graph': 'area', 
'Density Contour': 'density_contour','Heat Map': 'density_heatmap'} #names of plots mapped with their relevent Plotly functions
ops_dictionary = { "+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv } #operators available for custom graph (ratio etc) calculations

#Keep read function here so it only executes it ones and keep one list with all the data, don't end it, 
#Make copies of it for further work
#Use retrieveAllData function instead from the DataRetriever class to retrieve data from the database
#Retrieving data from local just for the local version
mainPath = os.path.dirname(os.path.realpath(__file__)) #the current directory
fofPath = os.path.join(mainPath, 'EVDSdata.xlsx') #Flow of Funds data
monthlyBalanceSheetPath = os.path.join(mainPath, 'BalanceSheet-Monthly.xlsx') #Balance of Payments Monthly Data
annualBalanceSheetPath = os.path.join(mainPath, 'BalanceSheet-Annual.xlsx') #Balance of Payments Annual Data
balanceSheetAssetsPath = os.path.join(mainPath, 'CB-2006-19-monthly-Analytical_Cleaned.xlsx') #Balance Sheet Data Assets (sheet 0)
balanceSheetLiabilitiesPath = os.path.join(mainPath, 'CB-2006-19-monthly-Analytical_Cleaned.xlsx') #Balance Sheet Data Liabilities (sheet 1)

#this function resets the variables to start off fresh
def reset():
    global counterSector, counterSectorArray, showPredictions, selectedPreviousDataName, selectedDataName, \
     selectedSectors, selected_data, selectedImportantGraph, selectedPreviousImportantGraph, timeFrame_column_names, sectors, \
     selectedSectorsDefinitions, importantGraphs, importantGraphDescription
    counterSector = 1
    counterSectorArray = [counterSector]
    showPredictions = False
    selectedPreviousDataName = None
    selectedDataName = None
    selectedSectors = [None,None,None,None]
    selected_data = [None,None,None,None]
    selectedImportantGraph = None
    selectedPreviousImportantGraph = None
    timeFrame_column_names = []
    sectors = []
    selectedSectorsDefinitions = [None,None,None,None]
    importantGraphs = {}
    importantGraphDescription = None

#this function populates the array with summaries from Wikipedia API
def fillDefinitions():
    global selectedSectorsDefinitions
    global selectedDataDefinition
    for i in range(counterSector): #for all sectors selected
        s =  selectedSectors[i] #retrieve the name
        if(s!=None): 
            #clean the string so that it can be searched using the API 
            s = s.split('.')[-1]  
            if "(Thousand TRY)" in s: 
                s = s.replace('(Thousand TRY)', '')
            elif "(Million USD)" in s: 
                s = s.replace('(Million USD)', '')
            elif "(Thousand TL)" in s: 
                s = s.replace('(Thousand TL)', '')
            
            try:
                selectedSectorsDefinitions[i] = wikipedia.summary(s, sentences=2) #You can easily increase the number of sentences
            except:
                selectedSectorsDefinitions[i] = "Definition not available" #if couldn't find summary for fitlered string

    try:
        selectedDataDefinition = wikipedia.summary(selectedDataName, sentences=1) #to receive definitions for data sheets
    except:
        selectedDataDefinition = "Definition not available" 
    
    print("selectedDataDefinition",selectedDataDefinition)

#this function runs everytime a data sheet is changed and retrieves the latest saved important graphs
def getImportantGraphsRequest(request):
    global importantGraphs
    #to get the data for the important graphs from our database
    retrievedImportantData = DataRetrieve.DataRetriever.pullFromTable(request.user.username, selectedDataName,"important_request")

    lenImportantData = len(retrievedImportantData)

    #for each retrieved ResultProxy (retrieved datatype), clean it up and retrieve necessary information like important graph name, description, its specific data sheet etc
    if(lenImportantData>0):
        for i in range(lenImportantData):
            sectorsString = (str(retrievedImportantData[i][0]))[:-1] #remove the ending comma for the sector
            usedSectorsList = sectorsString.split(",") #to retrieve a list of all the sectors used to generate this important graph
            graphName = str(retrievedImportantData[i][1])
            importantGraphs[graphName] = usedSectorsList #populates the dictionary mapping each important graph name to the used sectors for it
            importantGraphDescriptions[graphName] = str(retrievedImportantData[i][2]) #fills up an array containing the description for each of them

#handle the AJAX request for when a data sheet is selected
def handleDataSourceGraphRequest(request):
    global selectedPreviousDataName, selectedDataName, a, dataNames, importantGraphs

    selectedPreviousDataName = selectedDataName
    selectedDataName = request.GET.get('datas')
    if selectedDataName != None:
        if selectedDataName != selectedPreviousDataName:
            importantGraphs = {}
            #load the data from specificed paths. Use DataRetriever to get it from database for the version uploaded to server.
            if selectedDataName == dataNames[0]:
                a = pd.read_excel(fofPath)
            elif selectedDataName == dataNames[1]:
                a = pd.read_excel(monthlyBalanceSheetPath)
            elif selectedDataName == dataNames[2]:
                a = pd.read_excel(annualBalanceSheetPath)
            elif selectedDataName == dataNames[3]:
                a = pd.read_excel(balanceSheetAssetsPath)
            elif selectedDataName == dataNames[4]:
                a = pd.read_excel(balanceSheetLiabilitiesPath, sheet_name=1)
            
            
    else:
        selectedDataName = dataNames[0] #revert to fof data in case nothing selected
        a = pd.read_excel(fofPath)
    
    if(selectedDataName != None and selectedDataName != selectedPreviousDataName):
        #retrieve all custom saved graphs for the logged in user
        retrievedCustomData = DataRetrieve.DataRetriever.pullFromTable(request.user.username, selectedDataName,"custom_request")

        lenCustomData = len(retrievedCustomData)
        #Processing the ResultProxy datatype and converting it into a dataframe
        if(lenCustomData>0):
            for i in range(lenCustomData):
                retrievedString = retrievedCustomData[i][0]
                retrieveDF = pd.read_csv(StringIO(retrievedString))
                a = pd.concat([a,retrieveDF])

        getImportantGraphsRequest(request)

#handle AJAX request for when user wants to save an important graph to their account
def saveImportantGraphRequest(request):
    requestGet = request.GET.get('saveImportant')
    if (requestGet!= None):
        newEntryName = request.GET.get('inputImportantName')
        usedGraphs = ""
        #retrieve all the selected sectrors and convert them into a comma-separated string to save to database
        if(newEntryName !=""):
            for i in range(counterSector):
                dropDownUIName = "sectors" + str(i+1) #names of dropdowns for selected sectors
                sectorName = request.GET.get(dropDownUIName)
                usedGraphs = usedGraphs + sectorName +","
            
            importantDescription = request.GET.get('inputImportantDescription')
            datasource = request.GET.get('datas')
            DataRetrieve.DataRetriever.pushToTable("", request.user.username, datasource, "important_request", usedGraphs, importantDescription, newEntryName) #push entry to important graphs table in database
            getImportantGraphsRequest(request)

#handle AJAX request for when user wants to save a custom generated graph to their account
def handleCustomGraphRequest(request):
    global a, selectedImportantGraph, columnsList, valuesList

    requestGet = request.GET.get('saveCustom')
    if (requestGet!= None):
        newEntryName = request.GET.get('inputEntryName')
        if(newEntryName != ""):
            #retrieve selected custom entries and the operator for calculation
            customSector1Name = request.GET.get('sectors1custom')
            customSector2Name = request.GET.get('sectors2custom')
            operator = request.GET.get('operatorCustom')
            datasource = request.GET.get('datas')

            #clean up retrieved rows to retrieve values from them and perform the operation on each corresponding cell
            firstEntry = a[a['Entry'] == customSector1Name]
            firstEntryVals = firstEntry.drop(firstEntry.columns[[0, 1]], axis=1).values
            secondEntry = a[a['Entry'] == customSector2Name]
            secondEntryVals = secondEntry.drop(secondEntry.columns[[0, 1]], axis=1).values
            
            #perform operation on cleaned rows
            newEntry = ops_dictionary[operator](firstEntryVals, secondEntryVals)
            
            #data manipulation necessary to be able to save data to our database and match it up with the available dataframes
            columnsList = (firstEntry.iloc[:,2:].columns).tolist()
            columnsList.insert(0,'Entry')

            valuesList = newEntry.tolist()[0]
            valuesList.insert(0, newEntryName)

            pushFrameVals = (pd.DataFrame(valuesList, index=[columnsList], columns=[2]).T)
            pushFrameVals.columns = columnsList

            columnsList.insert(0, 'Unnamed: 0')

            valuesList.insert(0, 2)

            sumFrameVals = (pd.DataFrame(valuesList, index=[columnsList], columns=[len(a.index)]).T)
            
            sumFrameVals.columns = columnsList
            
            #push to database
            dataFrameInfo = pushFrameVals.to_csv() 
            DataRetrieve.DataRetriever.pushToTable(dataFrameInfo, request.user.username, datasource, "custom_request", "", "", "")
            
            #append to dataframe in current instance as well for instant update (to allow a smooth transition)
            a = pd.concat([a,sumFrameVals])

#handle user's AJAX request for an important graph
def handleImportantGraphRequest(request):
    global selectedImportantGraph, selectedPreviousImportantGraph, counterSector, counterSectorArray, selectedSectors, importantGraphDescription
    selectedPreviousImportantGraph = selectedImportantGraph
    selectedImportantGraph = request.GET.get('importantGraph')
    if(selectedImportantGraph!=None and selectedImportantGraph!="Choose..." and selectedImportantGraph!=selectedPreviousImportantGraph):
        #since we populate the important graphs dictionary when we load the datasheets to avoid continuous database connections
        #and allow smooth retrievel, you can retrieve required information from the populated dictionary at this step
        usedSectors=importantGraphs[selectedImportantGraph]
        importantGraphDescription=importantGraphDescriptions[selectedImportantGraph]
        counterSector = len(usedSectors)
        counterSectorArray = []
        #to select the sectors used to create the important graph
        for i in range(counterSector):
            selectedSectors[i] = usedSectors[i]
            counterSectorArray.append(i+1)

        #populate the corresponding sector lists
        handleListingRequest(request, True)
    else:
        handleListingRequest(request,False)
        
#assign prediction boolean based on request to be used while generating the graph
def handlePredictionRequest(request):
    global selectedPredictionMode, predictionModes, showPredictions

    selectedPredictionMode = request.GET.get('makePredictions')
    if selectedPredictionMode != None:
        if selectedPredictionMode == predictionModes[0]:
            showPredictions = False
        elif selectedPredictionMode == predictionModes[1]:
            showPredictions = True

#allow you to append or remove sectors from the list based on user request
def handleAddRemoveSectorRequest(request):
    global counterSector, counterSectorArray

    #handling button requests addSector-removeSector
    if (request.GET.get('addSector') != None):
        if (counterSector != 4):
            counterSector = counterSector + 1
            counterSectorArray.append(counterSector)
    if (request.GET.get('removeSector') != None):
        if (counterSector != 1):
            counterSector = counterSector - 1
            counterSectorArray.pop()

#this function populates the sector related arrays finally after all data manipulation is completed
def handleListingRequest(request, imp):
    global selectedSectors, sectors, selectedImportantGraph, selected_data

    if(not imp):
        selectedSectors[0] = sectors[0]

    for i in counterSectorArray:
        if(not imp):
            selectedSectors[i-1] = sectors[i]
            requestString = 'sectors' + str(i)

            if (request.GET.get(requestString) != None and selectedDataName == selectedPreviousDataName):
                selectedSectors[i-1] = request.GET.get(requestString)
            
        selected_data[i-1] = a[a['Entry'] == selectedSectors[i-1]]
        selected_data[i-1].drop(selected_data[i-1].columns[[0, 1]], axis=1, inplace=True)
        


@csrf_exempt
def home(request, copy=None):
    global timeFrame_column_names, sectors, a

    #on page reload, clean up selections
    if (not request.is_ajax()):
        reset()

    #this order is important
    handleDataSourceGraphRequest(request)
    handleCustomGraphRequest(request)
    saveImportantGraphRequest(request)
    handlePredictionRequest(request)
    handleAddRemoveSectorRequest(request)
    
    timeFrame_column_names = a.columns[a.columns.str.startswith('20', na=False)] #retrieve column names
    sectors =  a[a.columns[1]]
    
    handleImportantGraphRequest(request)
    fillDefinitions()

    #returns parameters required for the selected chart type
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

    #Allows you to forecast using an ARIMA model
    #All accuracy tests have been implemented in a separate module
    def makePredictions(sectorsData): 
        #filtering data
        dates = sectorsData['years']
        futureStepsN = int(request.GET.get('predictionTime')) #decide how many timeframes further the prediction should be
        forecastDates = []
        lastDate = dates[-1]

        #determines the seasonality parameter depending on timeframe difference in each specific data sheet
        #determines the period of difference to determine how much further is each futurestep (3 months for quarterly data, 1 year for yearly data etc)
        seasonality_m=4
        periodDifference=91
        if(selectedDataName == dataNames[0]):
            periodDifference = 91
            seasonality_m=4
        elif(selectedDataName == dataNames[1] or selectedDataName == dataNames[3] or selectedDataName == dataNames[4]):
            periodDifference = 30
            seasonality_m=12
        elif(selectedDataName == dataNames[2]):
            periodDifference = 365
            seasonality_m=1

        #Determine dates for each future timeframe based on the difference of days between each timeframe in the specific datasheet selected
        for i in range(futureStepsN):
            lastDate = lastDate + datetime.timedelta(days=periodDifference)
            forecastDates.append(lastDate)
        
        #a series of data manipulation to fit our values to the used model

        forecastDates = pd.to_datetime(forecastDates)
        sectorsData['years'] = sectorsData['years'].append(forecastDates)
        
        for i in counterSectorArray:
            sectorName = 'Sector ' + str(i)
            values = sectorsData[sectorName]

            #creating data frame
            data = pd.DataFrame(
                {'dates': dates,
                'values': values
                })

            data.set_index('dates', inplace=True)
            train = data
    
            arima = pm.auto_arima(train, seasonal=True, m=seasonality_m, error_action='ignore', trace=True,
                                suppress_warnings=True, maxiter=10)
            #keep the maxiter to a small number because the prediction happens in the realtime. For future expansion of
            #this project, the user can be allowed to select maxiter from UI based on the accuracy of prediction they want to attain
            
            forecastValues = arima.predict(futureStepsN)
            
            forecast_data = pd.Series(forecastValues, index = forecastDates) 

            sectorsData[sectorName] = sectorsData[sectorName].append(forecast_data)

        return sectorsData

    #provides plotly all the required parameters in a very clean fashion using dictionaries 
    def drawChart(chartType):
        x = pd.to_datetime(timeFrame_column_names) #for x axis
        data = {'years': x}

        #set of values for each sector for each time frame
        for i in counterSectorArray:
            sectorName = 'Sector ' + str(i)
            y = selected_data[i-1].iloc[0]
            y.index = x
            data[sectorName] = y

        if (showPredictions):
            data = makePredictions(data)
            
        #converting into a plotly compatible format annd retrieving parameters from our other functions
        df= (pd.DataFrame.from_dict(data,orient='index').transpose()).melt(id_vars="years")

        params = getParams(chartType)        

        fig = getattr(px, plotDictionary[chartType])(
                df,
                **params
            )

        fig.update_layout(height=520, width=800, paper_bgcolor='rgba(0,0,0,0)')

        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return plot_div

    if request.GET.get('plots') is None:
        getSelectedPlot = drawChart(list(plotDictionary.keys())[0])
    else:
        getSelectedPlot = drawChart(request.GET.get('plots'))

    

    context = {
        #returning all arrays along with certain 'specific' array entries and keys for easy access
        'plot': getSelectedPlot,
        'sectors': sectors,

        'selectedSector1': selectedSectors[0],
        'selectedSector2': selectedSectors[1],
        'selectedSector3': selectedSectors[2],
        'selectedSector4': selectedSectors[3],
        'selectedSectors': selectedSectors,

        'counterSectorArray': counterSectorArray,
        'plotTypes': plotDictionary.keys(),
        'selectedPlot': request.GET.get('plots'),
        'dataNames': dataNames,
        'selectedDataName': selectedDataName,
        'importantGraphs': importantGraphs.keys(),
        'selectedImportantGraph': selectedImportantGraph,
        'selectedPredictionMode': selectedPredictionMode,

        'selectedSectorsDefinitions1': selectedSectorsDefinitions[0],
        'selectedSectorsDefinitions2': selectedSectorsDefinitions[1],
        'selectedSectorsDefinitions3': selectedSectorsDefinitions[2],
        'selectedSectorsDefinitions4': selectedSectorsDefinitions[3],
        'selectedSectorsDefinitions': selectedSectorsDefinitions,
        'selectedDataDefinition': selectedDataDefinition,
        'importantGraphDescription': importantGraphDescription
    }
    if request.is_ajax():
        #return any required data using ajax to allowed $.get response in frontend after a request is made
        context['sectors'] = sectors.tolist()
        context['plotTypes'] = list(plotDictionary.keys())
        context['importantGraphs'] = list(importantGraphs.keys())
        context['makePredictions'] = predictionModes
        context['selectedDataName'] = selectedDataName

        return HttpResponse(json.dumps(context))
    else:
        return render(request, 'home/dashboard.html', context)