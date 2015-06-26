#-*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

import views

urlpatterns = [
    url(r'^add/' , views.user_add),
] 
