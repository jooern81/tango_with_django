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
from django.urls import include, path,re_path
from rango import views
from rango import urls
from django.conf import settings
from django.conf.urls.static import static
from django_registration.backends.one_step.views import RegistrationView

class RangoRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return "/rango/register_profile"

urlpatterns = [
    path('rango/', include('rango.urls')),      #this takes all the urls from the app rango and includes it as a reference url
    path('admin/', admin.site.urls),
    path('accounts/register/',RangoRegistrationView.as_view(success_url='/rango/register_profile'),name='django_registration_register'),
    path('accounts/', include('django_registration.backends.one_step.urls')), #links referenced to the package {% url 'django_registration_register' %}
    path('accounts/', include('django.contrib.auth.urls')), #links referenced directly "{% url 'login' %}"
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


