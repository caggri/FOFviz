from django.shortcuts import render
from plotly.offline import plot
import plotly.graph_objects as go

# Create your views here.

def table(request):
    context = {"table": "<h1>random</h1>"}

    return render(request, 'tables/datatable.html', context)


