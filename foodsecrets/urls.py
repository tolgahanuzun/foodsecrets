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
    url(r'^home/filter/$', 'profiles.views.filter'),
    url(r'^home/account/user/$', 'profiles.views.accountUser'),
    url(r'^home/account/password/$', 'profiles.views.accountPassword'),
    url(r'^home/account/image/$', 'profiles.views.accountImage'),
    url(r'^home/blockuser/(?P<username>[\w]+)$', 'profiles.views.blockUserToggle'),
    url(r'^home/favourite/toggle/(?P<key>[\d]+)$', 'profiles.views.favouriteToggle'),
    url(r'^home/follow/toggle/(?P<username>[\w]+)$', 'profiles.views.followToggle'),
    url(r'^home/follow/requesttoggle/(?P<username>[\w]+)$', 'profiles.views.request_followToggle'),
    url(r'^home/request/accept/(?P<username>[\w]+)$', 'profiles.views.acceptRequest'),
    url(r'^home/request/cancel/(?P<username>[\w]+)$', 'profiles.views.cancelRequest'),
    url(r'^home/favourites/$', 'profiles.views.myFavourites'),
    url(r'^home/mostfavourites/$', 'profiles.views.mostFavourites'),
    url(r'^home/followers/$', 'profiles.views.myFollowers'),
    url(r'^home/following/$', 'profiles.views.myFollowing'),
    url(r'^home/friendrequests/$', 'profiles.views.friendRequests'),
    url(r'^home/addmeal/$', 'foods.views.addMeal'),
    url(r'^home/meals/$', 'profiles.views.myMeals'),
    url(r'^home/meal/(?P<key>[\d]+)$', 'foods.views.showMeal'),
    url(r'^home/(?P<username>[\w]+)/$', 'profiles.views.showProfile'),
    url(r'^home/(?P<username>[\w]+)/(?P<mod>[\w]+)/$', 'profiles.views.showProfile'),
    url(r'^test/$',views.test),
    url(r'^page/$',views.page),
    url(r'^userpanel/$',views.userpanel),
]   
    