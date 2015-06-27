#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import *
from .forms import *

def register(request):
    error = 0

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():

            if form.clean_email(): 
               form.save()
            else:
               return render(request, "register.html",
                               { 'form':form, 'title':u'Kullanıcı Ekleme'})

            return HttpResponseRedirect('/register/') # Parametre olarak verilen url'e geçer.
        
        else:
            return render(request, "register.html",
                            { 'form':form, 'title':u'Kullanıcı Ekleme'})
    else:
        form = RegistrationForm()
        return render(request, "register.html",
                      { 'form':form, 'title':u'Kullanıcı Ekle'})

