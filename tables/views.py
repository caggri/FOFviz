from django.shortcuts import render
import pandas as pd
import os.path
import sys
sys.path.append("..")
import DataRetrieve

selectedTimeFrame = None
# Create your views here.

global all_data
retriever = DataRetrieve.DataRetriever("records")
all_data = retriever.retrieve()

def table(request):
    global selectedTimeFrame
   
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(path, 'EVDSdata.xlsx')
  
    #all_data = pd.read_excel(path)
    
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

