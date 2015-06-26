#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context, RequestContext, loader
from django.shortcuts import render

def index(request):
   

    return render(request, 'index.html')

def register(request):


    return render(request, 'register.html')
