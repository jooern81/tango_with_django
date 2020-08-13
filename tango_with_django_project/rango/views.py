from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("TIME TO GO HOME!" + "<a href='about'> ABOUT </a>") #

def about(request):
    return HttpResponse("WHAT IS THIS WEBSITE ABOUT" + "<a href='index'> INDEX </a>") #

# Create your views here.
