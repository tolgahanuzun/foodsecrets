#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

from .models import *
from .forms import *
from foods.models import Food

# Kullanıcı girişini yapan fonksiyon.
def login(request):

    if request.method == "POST":
        form_login = LoginForm(request.POST)

        if form_login.is_valid():  
            auth_login(request, form_login.user)

            return HttpResponseRedirect("/home/")
        else: 
            return render(request, "index.html", {'form_login':form_login})
    else:
        form_login = LoginForm()
        return render(request, "index.html", {'form_login':form_login})

# Çıkış fonksiyonu.
def logout(request):
    form_login = LoginForm()
    auth_logout(request)
    
    return HttpResponseRedirect("/")

# Kullanıcı kaydı yapan fonksiyon.
def register(request):

    #  Kullanıcı kayıt sayfasında login formunu görüntüleyebilmek için tanımlandı.
    form_login = LoginForm()

    if not request.user.is_authenticated():

        if request.method == 'POST':
            form_register = RegistrationForm(request.POST)

            if  form_register.is_valid():
            
                if not request.user.is_authenticated():
                    user = form_register.save()
                    auth_login(request, user)

                    return HttpResponseRedirect('/home/') # Parametre olarak verilen url'e geçer.
                else:
                    return HttpResponse("Şuan bir kullanıcı zaten aktif.")
        
            else:
                values = form_register.previous_values()
                return render(request, "register.html",
                               { 'form_register':form_register, 'form_login':form_login,
                            'values':values})
        else:
            form_register = RegistrationForm()
            return render(request, "register.html",
                          { 'form_register':form_register, 'form_login':form_login})

    else:
        ##############################################
        #     Güzel bir hata mesajı verdirilecek     #
        ##############################################
        return HttpResponseRedirect("/")

def accountUser(request):
    if request.user.is_authenticated():

        if request.method == "POST":
            form_accountUser = AccountFormUser(request.POST, user=request.user)

            if form_accountUser.is_valid():

                form_accountUser.change()

                return render(request, "account.html", {'form_accountUser':form_accountUser}) 

            else:
                return render(request, "account.html", {'form_accountUser':form_accountUser}) 
        else:
            form_accountUser = AccountFormUser()
            return render(request, "account.html", {'form_accountUser':form_accountUser})

    else:
        return HttpResponseRedirect("/")


def accountPassword(request):
    if request.user.is_authenticated():

        if request.method == "POST":
            form_accountPassword = AccountFormPassword(request.POST, user=request.user)
 
            form_accountPassword.setValue()
            if form_accountPassword.is_valid():
                
                form_accountPassword.change()
                auth_login(request, form_accountPassword.user)

                return render(request, "account.html", {'form_accountPassword':form_accountPassword}) 
  
            else:
                return render(request, "account.html", {'form_accountPassword':form_accountPassword}) 
        
        else:
            form_accountPassword = AccountFormPassword()
            return render(request, "account.html", {'form_accountPassword':form_accountPassword})
    
    else:
        return HttpResponseRedirect("/")

def home(request):
    
    AllMeal = Food.objects.all()

    if request.user.is_authenticated():
        return render(request, "home.html", {'AllMeal':AllMeal})
    else:
        return HttpResponseRedirect("/")



