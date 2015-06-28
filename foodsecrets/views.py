#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Template, Context, RequestContext, loader
from django.shortcuts import render
from profiles.forms import LoginForm

# Ana Sayfa'yı görüntüleyen fonksiyon.
def index(request):
    # Ana sayfada login formunun görüntüleyebilmek için tanımlandı.
    form_login = LoginForm()

    return render(request, 'index.html', {'form_login':form_login})
