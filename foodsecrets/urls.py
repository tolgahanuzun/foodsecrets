"""foodsecrets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^register/$', 'profiles.views.register'),
    url(r'^login/$', 'profiles.views.login'),
    url(r'^logout/$', 'profiles.views.logout'),
    url(r'^home/$', 'profiles.views.home'),
    url(r'^home/search/$', 'profiles.views.search'),
    url(r'^home/(?P<username>[\w]+)$', 'profiles.views.showProfile', name='user_profile'),
    url(r'^home/filter/$', 'profiles.views.filter'),
    url(r'^home/account/user/$', 'profiles.views.accountUser'),
    url(r'^home/account/password/$', 'profiles.views.accountPassword'),
    url(r'^home/account/image/$', 'profiles.views.accountImage'),
    url(r'^home/favourite/toggle/(?P<key>[\d]+)$', 'profiles.views.favouriteToggle'),
    url(r'^home/myfavourites/$', 'profiles.views.myFavourites'),
    url(r'^home/mostfavourites/$', 'profiles.views.mostFavourites'),
    url(r'^home/addmeal/$', 'foods.views.addMeal'),
    url(r'^home/mymeals/$', 'profiles.views.myMeals'),
    url(r'^home/meal/(?P<key>[\d]+)$', 'foods.views.showMeal'),
    url(r'^test/$',views.test),
    url(r'^page/$',views.page),
    url(r'^userpanel/$',views.userpanel),
]   
    