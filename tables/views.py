from django.shortcuts import render
import pandas as pd
import os.path

selectedTimeFrame = None
# Create your views here.
def table(request):
    global selectedTimeFrame
        
    all_data = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + '\EVDSdata.xlsx')
    if selectedTimeFrame is None:
        selectedTimeFrame = all_data.columns[-1]
    else:
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

