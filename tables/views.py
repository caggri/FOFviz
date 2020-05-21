from django.shortcuts import render
import pandas as pd
import numpy as np
import os.path
import sys
from sklearn.svm import SVR
sys.path.append("..")
import DataRetrieve
import matplotlib.pyplot as plt

selectedTimeFrame = None
selectedDataName = None

# paths for attaining data from local
fofPath = os.path.dirname(os.path.realpath(__file__))
fofPath = os.path.join(fofPath, 'EVDSdata.xlsx')

monthlyBOPPath = os.path.dirname(os.path.realpath(__file__))
monthlyBOPPath = os.path.join(monthlyBOPPath, 'BalanceSheet-Monthly.xlsx')

annualBOPPath = os.path.dirname(os.path.realpath(__file__))
annualBOPPath = os.path.join(annualBOPPath, 'BalanceSheet-Annual.xlsx')

balanceSheetPath = os.path.dirname(os.path.realpath(__file__))
balanceSheetPath = os.path.join(balanceSheetPath, 'CB-2006-19-monthly-Analytical_Cleaned.xlsx')

# use this to retrieve data from the database
# retriever = DataRetrieve.DataRetriever()
# all_data = retriever.retrieve()
# load_all_data = pd.read_excel(path)

dates = []
prices = []
#initiliazing types of sheets
dataNames = ['Flow of Funds', 'Balance of Payment (Annual)', 'Balance of Payment (Monthly)', 'Balance Sheet']
#initializing important currencies and their patterns
currencyNames = [['Assets (Thousand TRY)','Liabilities (Thousand TRY)'],['Assets (Million USD)','Liabilities (Million USD)'],['Assets (Thousand TL)','Liabilities (Thousand TL)']]
currencyPatternList = ["\(Thousand TRY\)","\(Million USD\)","\(Thousand TL\)"]
# Create your views here.

#this loads all of the data available, must be moved to inital page.
# load_all_data = DataRetrieve.DataRetriever.retrieveAllData()

def table(request):
    global selectedDataName #the name of the data sheet selected
    global selectedPreviousDataName
    global selectedTimeFrame #time frame for which values are to be shown
    global all_data #contains all the excel data to be filtered
    global assets_bs #balance sheet data is split into assets and liabilities using different excel sheets
    global liabilities_bs
    global dates
    global prices
    global dataNames
    global currencyNames
    global currency
    global currencyPatternList
    global currencyPattern

    if(request.GET.get('dataName') != None):
        selectedPreviousDataName = selectedDataName
        selectedDataName = request.GET.get('dataName')
    else:
        selectedDataName = dataNames[0]

    #read the selected data sheet and the corresponding currency
    if selectedDataName == dataNames[0]:
        all_data = pd.read_excel(fofPath)
        currency = currencyNames[0]
        currencyPattern = currencyPatternList[0]
    elif selectedDataName == dataNames[1] or selectedDataName == dataNames[2]:
        if selectedDataName == dataNames[1]:
            all_data = pd.read_excel(annualBOPPath)
        else:
            all_data = pd.read_excel(monthlyBOPPath)
        currency = currencyNames[1]
        currencyPattern = currencyPatternList[1]
    elif selectedDataName == dataNames[3]:
        #clean data and adjust format according to requirements of displaying balance sheet
        currency = currency = currencyNames[2]
        currencyPattern = currencyPatternList[2]
        assets_bs = pd.read_excel(balanceSheetPath)
        assets_bs = assets_bs.dropna(how='all') #drop rows whose columns are all NaN
        liabilities_bs = pd.read_excel(balanceSheetPath, sheet_name=1)
        liabilities_bs = liabilities_bs.dropna(how='all') #drop rows whose columns are all NaN
        liabilities_bs = liabilities_bs[:-1] #drop Time col
        assets_bs=assets_bs.drop(assets_bs[assets_bs.iloc[:, 0] == 'Computed Value'].index.values.astype(int)[0])
        assets_bs=assets_bs.drop(assets_bs[assets_bs.iloc[:, 0] == 'Time'].index.values.astype(int)[0])
        all_data = assets_bs #for timeframe
    
    #data formatting 
    if(request.GET.get('timeFrames') != None and selectedPreviousDataName == selectedDataName):
        selectedTimeFrame = request.GET.get('timeFrames')
    elif selectedDataName == dataNames[3]:
        selectedTimeFrame = assets_bs.columns[-1]
    else:
        selectedTimeFrame = all_data.columns[-1]
    
    if selectedDataName == dataNames[0]:
        #Formatting data for Flow of funds accounts
        assets_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ VF.\d\D')], columns=['Entry', selectedTimeFrame]) #find assets based on excel cell entry format - VF indicates asset
        liabilities_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ YF.\d\D')], columns=['Entry', selectedTimeFrame]) #find assets based on excel cell entry format - YF indicates liability
        assets_and_liabilities_data = pd.merge(assets_data, liabilities_data, on=assets_data.index, how='outer') #merging the two data sets
        assets_and_liabilities_data.columns = ['EntryNo','Assets (Thousand TRY)',selectedTimeFrame, 'Liabilities (Thousand TRY)', selectedTimeFrame] #displaying them according to the selected timeframe
    
    elif selectedDataName == dataNames[1] or selectedDataName == dataNames[2]:
        #Formatting data for Balance of Payments sheets
        assets_data = pd.DataFrame(all_data[all_data['Entry'].str.contains(pat = '^[ABD][.]', regex = True)], columns=['Entry', selectedTimeFrame]) #excel cell entries specify entries starting with A B and D as assets, clean data accordingly
        liabilities_data = pd.DataFrame(all_data[all_data['Entry'].str.contains(pat = '^[CE][.]', regex = True)], columns=['Entry', selectedTimeFrame]) #C and E as liabilities
        
        #continuing with manipulation necessary for making it compatible with our data display format
        assets_data.reset_index(drop=True, inplace=True) 
        liabilities_data.reset_index(drop=True, inplace=True)
        
        assets_and_liabilities_data = pd.concat([assets_data,liabilities_data], ignore_index=False, axis=1)
        assets_and_liabilities_data = assets_and_liabilities_data.replace(np.nan, '', regex=True)
        
        assets_and_liabilities_data.columns = ['Assets (Million USD)',selectedTimeFrame, 'Liabilities (Million USD)', selectedTimeFrame]
        
    elif selectedDataName == dataNames[3]:
        #Formatting data for balance sheet entries
        assets_data = pd.DataFrame(assets_bs, columns=['Unnamed: 0', selectedTimeFrame]) #Appending necessary columns to make it compatible with the format of our other sheets
        liabilities_data = pd.DataFrame(liabilities_bs, columns=['Unnamed: 0', selectedTimeFrame])

        #continuing with manipulation necessary for making it compatible with our data display format
        assets_data.reset_index(drop=True, inplace=True)
        liabilities_data.reset_index(drop=True, inplace=True)
        assets_and_liabilities_data = pd.concat([assets_data, liabilities_data], axis=1)
        assets_and_liabilities_data.columns = ['Assets (Thousand TL)',selectedTimeFrame, 'Liabilities (Thousand TL)', selectedTimeFrame]
        
    #Adjusting currency patterns for different data sheets
    assets_and_liabilities_data[currency[0]] = assets_and_liabilities_data[currency[0]].str.replace(currencyPattern,"")
    assets_and_liabilities_data[currency[1]] = assets_and_liabilities_data[currency[1]].str.replace(currencyPattern,"")
    
    context = {
            'table': assets_and_liabilities_data.to_html(table_id='dataTable', classes='table table-bordered', index=False),
            'timeFrames': all_data.columns[all_data.columns.str.startswith('20')],
            'selectedTimeFrame' : selectedTimeFrame,
            'selectedDataName': selectedDataName,
            'dataNames' : dataNames
        }

    return render(request, 'tables/datatable.html', context)
    
