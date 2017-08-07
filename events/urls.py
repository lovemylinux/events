"""events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.views import *
from django.conf.urls import handler404


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^invite/', invite),
    url(r'^404/', not_found),
    url(r'^invitation/([-A-Za-z0-9]{36})', decision),
    url(r'^profile$', change),
    url(r'^api/invitations/add$', add_invite),
    url(r'^api/invitations/edit', change_invite),
    url(r'^api/invitations/delete', delete_invite),
    url(r'^api/invitations/decision$', get_decision),
]

handler404 = handler404
