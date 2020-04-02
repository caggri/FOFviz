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

#path = os.path.dirname(os.path.realpath(__file__))
#path = os.path.join(path, 'EVDSdata.xlsx')
#retriever = DataRetrieve.DataRetriever()
#all_data = retriever.retrieve()
#all_data = pd.read_excel(path)

dates = []
prices = []
dataNames = ['Flow of Funds', 'Balance Sheet (Annual)', 'Balance Sheet (Monthly)']
currencyNames = [['Assets (Thousand TRY)','Liabilities (Thousand TRY)'],['Assets (Million USD)','Liabilities (Million USD)']]
currencyPatternList = ["\(Thousand TRY\)","\(Million USD\)"]
# Create your views here.

#this loads all of the data available, must be moved to inital page.
load_all_data = DataRetrieve.DataRetriever.retrieveAllData()

def table(request):
    global selectedDataName
    global selectedPreviousDataName
    global selectedTimeFrame
    global all_data
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

    if selectedDataName == dataNames[0]:
        all_data = DataRetrieve.DataRetriever.retrieveFofData()
        currency = currencyNames[0]
        currencyPattern = currencyPatternList[0]
    elif selectedDataName == dataNames[1] or selectedDataName == dataNames[2]:
        if selectedDataName == dataNames[1]:
            all_data = DataRetrieve.DataRetriever.retrieveAnnuallyData()
        else:
            all_data = DataRetrieve.DataRetriever.retrieveMonthlyData()
        currency = currencyNames[1]
        currencyPattern = currencyPatternList[1]

    if(request.GET.get('timeFrames') != None and selectedPreviousDataName == selectedDataName):
            selectedTimeFrame = request.GET.get('timeFrames')
    else:
        selectedTimeFrame = all_data.columns[-1]

    if selectedDataName == dataNames[0]:
        assets_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ VF.\d\D')], columns=['Entry', selectedTimeFrame])
        liabilities_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ YF.\d\D')], columns=['Entry', selectedTimeFrame])
        assets_and_liabilities_data = pd.merge(assets_data, liabilities_data, on=assets_data.index, how='outer')
        assets_and_liabilities_data.columns = ['EntryNo','Assets (Thousand TRY)',selectedTimeFrame, 'Liabilities (Thousand TRY)', selectedTimeFrame]
    elif selectedDataName == dataNames[1] or selectedDataName == dataNames[2]:
        assets_data = pd.DataFrame(all_data[all_data['Entry'].str.contains(pat = '^[ABD][.]', regex = True)], columns=['Entry', selectedTimeFrame])
        liabilities_data = pd.DataFrame(all_data[all_data['Entry'].str.contains(pat = '^[CE][.]', regex = True)], columns=['Entry', selectedTimeFrame])
        assets_data.reset_index(drop=True, inplace=True)
        liabilities_data.reset_index(drop=True, inplace=True)
        
        assets_and_liabilities_data = pd.concat([assets_data,liabilities_data], ignore_index=False, axis=1)
        assets_and_liabilities_data = assets_and_liabilities_data.replace(np.nan, '', regex=True)
        
        assets_and_liabilities_data.columns = ['Assets (Million USD)',selectedTimeFrame, 'Liabilities (Million USD)', selectedTimeFrame]
        
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

def predict_prices(dates, prices, x):
    dates = np.reshape(dates, (len(dates), 1))

    svr_lin = SVR(kernel='linear', C=1e3)
    svr_poly = SVR(kernel='poly', C=1e3, degree=2)
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma= 0.1)

    svr_lin.fit(dates, prices)
    svr_poly.fit(dates, prices)
    svr_rbf.fit(dates, prices)
    
    plt.scatter(dates, prices, color='black', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='red', label='RBF model')
    plt.plot(dates, svr_lin.predict(dates), color='green', label='Linear model')
    plt.plot(dates, svr_poly.predict(dates), color='blue', label='Polynomial model')

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Support Vector Regression')
    plt.legend()
    plt.show()

    return svr_rbf.predict(x)[0], svr_lin.predict(x)[0], svr_poly.predict(x)[0]
    
