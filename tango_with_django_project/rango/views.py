from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("TIME TO GO HOME!")

# Create your views here.
