"""learning URL Configuration

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
from .views import (home_view, login_view, register_view, logout_view, profile_view, 
    delete_view, follow_view, unfollow_view, edit_view, show_blogs_view, delete_blog_view)

urlpatterns = [
    url(r'^$', home_view, name='home'),
    url(r'^login', login_view, name='login'),
    url(r'^register', register_view, name='register'),
    url(r'^profile/(?P<username>\w+)/$', profile_view, name='profile'),
    url(r'^delete$', delete_view, name='delete'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^follow/(?P<username>\w+)/$', follow_view, name='follow'),
    url(r'unfollow/(?P<username>\w+)/$', unfollow_view, name='unfollow'),
    url(r'^profile/(?P<username>\w+)/editing/(?P<action>\w+)/$', edit_view, name='edit'),
    url(r'^profile/(?P<username>\w+)/blogs/$', show_blogs_view, name='show_blogs_view'),
    url(r'^profile/(?P<username>\w+)/blogs/delete/(?P<blog_id>\d+)/$', delete_blog_view, name='delete_blog_view'),
]
