#-*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context, RequestContext, loader
from django.shortcuts import render
from profiles.forms import *

# Ana Sayfa'yı görüntüleyen fonksiyon.
def index(request):
    if not request.user.is_authenticated():
        # Ana sayfada login formunun görüntüleyebilmek için tanımlandı.
        form_login = LoginForm()
        return render(request, 'index.html', {'form_login':form_login})
    else:
    	return HttpResponseRedirect("/home/")
    	