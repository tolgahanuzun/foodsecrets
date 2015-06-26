#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .models import *
from .forms import *

def user_add(request):
    error = 0

    if request.method == 'POST':
        #form = userAdd_form(request.POST)
        form = RegistrationForm(request.POST)
        
        if form.is_valid(): 
            data = form.cleaned_data

            if data.get("password") != data.get("password_again"):
                error = 1

            if error == 0:
            
                username = data.get('username')
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                email = data.get('email')
                password = data.get('password')
            
                user = User.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password
                )

                user_profile = Profile()
                user_profile.profile = user
                user_profile.phone = data.get('phone')
                user_profile.save()

                return HttpResponseRedirect('/user/add/')
            else:
                return render(request, "register.html",
                            { 'form':form, 'title':u'Kullanıcı Ekleme', 'error':error})
        else:
            return render(request, "register.html",
                            { 'form':form, 'title':u'Kullanıcı Ekleme', 'error':error})
    else:
        #form = userAdd_form()
        form = RegistrationForm()
        return render(request, "register.html",
                      { 'form':form, 'title':u'Kullanıcı Ekle'})

