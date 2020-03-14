from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

def landing(request):
    # <view logic>
    return render(request, 'landing/index.html', {})