"""Devops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from git import views as git_view
from cleancache import views as cleancache_view
from ops import views as ops_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', git_view.index),
    url(r'^develop/$', git_view.develop, name='develop'),
    url(r'^ccshop/(?P<id>[0-9]+)/$', git_view.ccshopissue, name='ccshop'),
    url(r'^themes/(?P<id>[0-9]+)/$', git_view.themes, name='themes'),
    url(r'^themesmobile/(?P<id>[0-9]+)/$', git_view.themes_mobile, name='themesmobile'),
    url(r'^login/$', git_view.login_site, name='login'),
    url(r'^logout/$', git_view.logout_site, name='logout'),
    url(r'^searchdomain/$', cleancache_view.searchdomain, name='searchdomain'),
    url(r'^cleancache/(?P<id>[0-9]+)/$', cleancache_view.cleancache, name='cleancache'),
    url(r'^opssearchdomain/$', ops_view.ops_search_domain, name='opssearchdomain'),
    url(r'^ops_operate/(?P<id>[0-9]+)/$', ops_view.ops_operate, name='aaa'),
    url(r'^testopssearchdomain/$', ops_view.test_ops_search_domain, name='testopssearchdomain'),
    url(r'^testopsoperate/(?P<id>[0-9]+)/$', ops_view.test_ops_operate, name='testopsoperate'),
]
