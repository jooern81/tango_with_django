import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_with_django_project.settings')

import pandas as pd
import numpy as np

import django
django.setup()
from rango.models import Category,Page, DemandForecast

def add_demandforecast(name,demand=0):     #build it such that can populate multiple tables from different csv files
    d = DemandForecast.objects.update_or_create(name=name)[0]
    d.demand = demand
    d.save()

def add_page(cat, title, url, views=0, likes=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0] #creates an instance if it doesn't already exist
    p.url=url
    p.views=views
    p.likes=likes
    p.save()
    return p

def add_cat(name,views,likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

def populate():
    python_pages = [
    {"title": "Official Python Tutorial",
    "url":"http://docs.python.org/2/tutorial/", "views":111, "likes":11},
    {"title":"How to Think like a Computer Scientist",
    "url":"http://www.greenteapress.com/thinkpython/", "views":222, "likes":22},
    {"title":"Learn Python in 10 Minutes",
    "url":"http://www.korokithakis.net/tutorials/python/", "views":333, "likes":33} ]

    django_pages = [
    {"title":"Official Django Tutorial",
    "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/", "views":444, "likes":44},
    {"title":"Django Rocks",
    "url":"http://www.djangorocks.com/", "views":555, "likes":55},
    {"title":"How to Tango with Django",
    "url":"http://www.tangowithdjango.com/", "views":666, "likes":66} ]

    other_pages = [
    {"title":"Bottle",
    "url":"http://bottlepy.org/docs/dev/", "views":128, "likes":64},
    {"title":"Flask",
    "url":"http://flask.pocoo.org", "views":128, "likes":64} ]

    cats = {"Python": {"pages": python_pages, "views":128, "likes":64},
    "Django": {"pages": django_pages, "views":32, "likes":16},
    "Other Frameworks": {"pages": other_pages,"views":64, "likes":32} }

    for cat, cat_data in cats.items():
        c = add_cat(cat,cat_data["views"],cat_data["likes"])
        for p in cat_data["pages"]:
            add_page(c, p["title"], p["url"],p["views"],p["likes"])

# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

# Import demand_forecast.csv data
    df = pd.read_csv("demand_forecast.csv")
    demand_list = df['Initial Demand']
    product = df['Product']

# Iterate through the csv data and insert all the entries based on the length of the csv dataframe
    for entry in range(0, len(demand_list)):
        d = add_demandforecast(product[entry],demand_list[entry]) #this must match the functions input sequence





# Start execution here!
if __name__ == '__main__':      #import code without running it, while also keeping it as an executable
    print("Starting Rango population script...")
    populate()