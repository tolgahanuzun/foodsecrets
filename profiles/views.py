#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.template.context_processors import csrf


from .models import *
from .forms import *

# Kullanıcı girişini yapan fonksiyon.
def login(request):

    if request.method == "POST":
        form_login = LoginForm(request.POST)

        if form_login.is_valid():
            auth_login(request, form_login.user)
            url = "/" + form_login.cleaned_data.get("username") + "/"
            return HttpResponse("Merhaba "+ form_login.cleaned_data.get("username"))
        else: 
            return HttpResponse("Hata!")
            #return render(request, "index.html", {'form_login':form_login})
    else:
        form_login = LoginForm()
        return render(request, "index.html", {'form_login':form_login})

# Çıkış fonksiyonu.
def logout(request):
    form_login = LoginForm()
    auth_logout(request)
    
    return render(request, "index.html", {'form_login':form_login})

# Kullanıcı kaydı yapan fonksiyon.
def register(request):

    #  Kullanıcı kayıt sayfasın'da login formunu görüntüleyebilmek için tanımlandı.
    form_login = LoginForm()

    if request.method == 'POST':
        form_register = RegistrationForm(request.POST)

        if form_register.is_valid():

            if form_register.clean_email(): 
               form_register.save()
               return HttpResponseRedirect('/register/') # Parametre olarak verilen url'e geçer.

            else:
               return render(request, "register.html",
                               { 'form_register':form_register, 'form_login':form_login})
        
        else:
            return render(request, "register.html",
                            { 'form_register':form_register, 'form_login':form_login})
    else:
        form_register = RegistrationForm()
        return render(request, "register.html",
                      { 'form_register':form_register, 'form_login':form_login})



