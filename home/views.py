from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go
import pandas as pd
import os.path

# Create your views here.

selectedSector = None
def home(request):
    global selectedSector
    all_data = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + '\EVDSdata.xlsx')
    timeFrame_column_names = all_data.columns[all_data.columns.str.startswith('20')]
    sectors =  all_data[all_data.columns[1]]

    if selectedSector is None:
        selectedSector = sectors[1]
    else:
        selectedSector = request.GET.get('sectors')

    selected_data = all_data[all_data['Entry'] == selectedSector]
    selected_data.drop(selected_data.columns[[0, 1]], axis=1, inplace=True)
    print(selected_data.iloc[0])

    def scatter():
        x1 = timeFrame_column_names
        y1 = selected_data.iloc[0]

        trace = go.Scatter(
            x=x1,
            y=y1
        )
        layout = dict(
            title='Line Plot',
            xaxis=dict(range=[min(x1), max(x1)]),
            yaxis=dict(range=[min(y1), max(y1)])
        )
        fig = go.Figure(data=[trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs = False)
        return plot_div

    context = {
        'plot': scatter(),
        'sectors': sectors,
        'selectedSector': selectedSector
    }

    return render(request, 'home/dashboard.html', context)
