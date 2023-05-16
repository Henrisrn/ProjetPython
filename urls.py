"""
URL configuration for monprojet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from . import views, page2views, page3views, page4views
from django.urls import path, re_path, include
from django_plotly_dash.views import add_to_session


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('django_plotly_dash/', include('django_plotly_dash.urls', namespace='django_plotly_dash')),
    re_path(r'^django_plotly_dash/', add_to_session),
    
    path('page2/', page2views.page2, name='page2'),
    path('page3/', page3views.page2, name='page3'),
    path('page4/', page4views.page2, name='page4'),
]