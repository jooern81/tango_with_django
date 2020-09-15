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

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from django.urls import path,re_path
from rango import views
from rango import urls
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rango'

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('about', views.about, name = 'about'),
    path('add_category', views.add_category, name='add_category'),
    path('add_page', views.add_page, name='add_page'),
    path('register', views.register, name='register'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('restricted', views.restricted, name='restricted'),
    path('goto', views.track_url, name='goto'),
    path('register_profile', views.register_profile, name='profile_registration'),
    path('list_profiles', views.list_profiles, name='list_profiles'),
    path('like', views.like_category, name='like_category'),
    re_path(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category, name='show_category'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/add_page$',views.add_page, name='add_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

