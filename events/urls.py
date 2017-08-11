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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf.urls.static import static
from django.conf import settings
from app.views import *


urlpatterns = [
    url(r'^$', show_index_page, name='index'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^invite/', show_create_invite_page, name='invite'),
    url(r'^invitation/([-A-Za-z0-9]{36})', show_invitation, name='show_invitation'),
    url(r'^dashboard$', show_dashboard_page, name='dashboard'),

    url(r'^api/invitations/add$', add_invite, name='api_add_invite'),
    url(r'^api/invitations/edit', change_invite, name='api_change_invite'),
    url(r'^api/invitations/delete', delete_invite, name='api_delete_invite'),
    url(r'^api/invitations/decision$', change_decision, name='api_change_decision'),

    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
