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

path = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(path, 'EVDSdata.xlsx')
#retriever = DataRetrieve.DataRetriever()
#all_data = retriever.retrieve()
all_data = pd.read_excel(path)

dates = []
prices = []

# Create your views here.

#this loads all of the data available, must be moved to inital page.
#load_all_data = DataRetrieve.DataRetriever.retrieveAllData()

#all_data = DataRetrieve.DataRetriever.retrieveFofData()

def table(request):
    global selectedTimeFrame
    global all_data
    global dates
    global prices

    selectedTimeFrame = all_data.columns[-1]
    
    if(request.GET.get('timeFrames') != None):
        selectedTimeFrame = request.GET.get('timeFrames')
        
    assets_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ VF.\d\D')], columns=['Entry', selectedTimeFrame])
    liabilities_data = pd.DataFrame(all_data[all_data['Entry'].str.contains('__ YF.\d\D')], columns=['Entry', selectedTimeFrame])
    assets_and_liabilities_data = pd.merge(assets_data, liabilities_data, on=assets_data.index, how='outer')
    assets_and_liabilities_data.columns = ['EnrtyNo','Assets (Thousand TRY)',selectedTimeFrame, 'Liabilities (Thousand TRY)', selectedTimeFrame]
    assets_and_liabilities_data['Assets (Thousand TRY)'] = assets_and_liabilities_data['Assets (Thousand TRY)'].str.replace("\(Thousand TRY\)","")
    assets_and_liabilities_data['Liabilities (Thousand TRY)'] = assets_and_liabilities_data['Liabilities (Thousand TRY)'].str.replace("\(Thousand TRY\)","")
    
    context = {
        'table': assets_and_liabilities_data.to_html(table_id='dataTable', classes='table table-bordered', index=False),
        'timeFrames': all_data.columns[all_data.columns.str.startswith('20')],
        'selectedTimeFrame' : selectedTimeFrame
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
    
