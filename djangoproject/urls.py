"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from . views import HomeView
from django.contrib.auth import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('grapher/', include('grapher.urls')),
    path('accounts/', include('accounts.urls')),
    path('ticker_manager/', include('ticker_manager.urls')),
    path('database_overview/', include('database_overview.urls')),
    path('', HomeView,name='home'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),

]  
