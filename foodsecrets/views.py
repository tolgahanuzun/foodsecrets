#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context, RequestContext, loader
from django.shortcuts import render

# Ana Sayfa'yı görüntüleyen fonksiyon.
def index(request):
   return render(request, 'index.html')
