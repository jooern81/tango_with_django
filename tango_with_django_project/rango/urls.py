#this additional url.py file within the app links all the links of the app to the rango app
#it is later referenced by the main project url.py file which calls for all urls from the rango app


"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rango import views
from django.conf.urls import url
from django.urls import path

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('about', views.about, name = 'about')
    
]
