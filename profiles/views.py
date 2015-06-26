#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import *
from .forms import *

# Kullanıcı kayıt işlemini yapan fonksiyon.
def register(request):
    error = 0

    if request.method == 'POST':
        #form = userAdd_form(request.POST)
        form = RegistrationForm(request.POST)
        
        # Gönderilen formun utgun olup olmadığı kontrol ediliyor.
        if form.is_valid(): 
            data = form.cleaned_data

            # Girilen şifrelerin aynı olup olmadığı kontrol ediliyor.
            if data.get("password") != data.get("password_again"):
                error = 1

            # Mail adresi daha önceden kaydedilmiş mi kontrol ediliyor.
            profiles_email = User.objects.filter(email=data.get('email'))
            if profiles_email:
                error = 2

            # Girilen username'e sahip kullanıcı var mı kontrol ediliyor.
            profiles_username = User.objects.filter(username=data.get('username'))
            if profiles_username:
                error = 3

            # Hata yoksa kişi kayıt işlemi gerçekleşiyor.
            if error == 0:
                user = User.objects.create_user(
                    username = data.get('username'),
                    first_name = data.get('first_name'),
                    last_name = data.get('last_name'),
                    email = data.get('email'),
                    password = data.get('password')
                )

                user_profile = Profile()
                user_profile.profile = user
                user_profile.phone = data.get('phone')
                user_profile.save()

                return HttpResponseRedirect('/user/add/') # Parametre olarak verilen url'e geçer.
            else:
                # Uygun olan formda yukarıdaki  hatalardan biri varsa gerekli hata mesajları ile 
                # form gösteriliyor.
                return render(request, "register.html",
                            { 'form':form, 'title':u'Kullanıcı Ekleme', 'error':error})
        else:
            # Form uygun değilse ona göre hata mesajları ile beraber form gösteriliyor.
            return render(request, "register.html",
                            { 'form':form, 'title':u'Kullanıcı Ekleme', 'error':error})
    else:
        # Herhangi bir 'POST' isteği yoksa boş form gösteriliyor.

        #form = userAdd_form()
        form = RegistrationForm()
        return render(request, "register.html",
                      { 'form':form, 'title':u'Kullanıcı Ekle'})

