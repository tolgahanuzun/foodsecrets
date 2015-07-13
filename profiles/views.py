#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from foods.models import Meal

import re

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
            
                user = form_register.save()
                auth_login(request, user)

                return HttpResponseRedirect('/home/') # Parametre olarak verilen url'e geçer.
        
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
        return HttpResponseRedirect("/home/")

def accountUser(request):
    if request.user.is_authenticated():

        form_accountImage = AccountFormImage()
        if request.method == "POST":
            form_accountUser = AccountFormUser(request.POST, user=request.user)

            if form_accountUser.is_valid():

                form_accountUser.change()

                return render(request, "account.html", {'form_accountUser':form_accountUser, 
                                                        'form_accountImage':form_accountImage}) 

            else:
                return render(request, "account.html", {'form_accountUser':form_accountUser, 
                                                        'form_accountImage':form_accountImage}) 
        else:
            form_accountUser = AccountFormUser()
            return render(request, "account.html", {'form_accountUser':form_accountUser, 
                                                        'form_accountImage':form_accountImage}) 

    else:
        return HttpResponseRedirect("/")


def accountPassword(request):
    if request.user.is_authenticated():

        form_accountImage = AccountFormImage()
        if request.method == "POST":
            form_accountPassword = AccountFormPassword(request.POST, user=request.user)
 
            form_accountPassword.setValue()
            if form_accountPassword.is_valid():
                
                form_accountPassword.change()
                auth_login(request, form_accountPassword.user)

                return render(request, "account.html", {'form_accountPassword':form_accountPassword, 
                                                        'form_accountImage':form_accountImage}) 
            else:
                return render(request, "account.html", {'form_accountPassword':form_accountPassword, 
                                                        'form_accountImage':form_accountImage}) 
        else:
            form_accountPassword = AccountFormPassword()
            return render(request, "account.html", {'form_accountPassword':form_accountPassword, 
                                                        'form_accountImage':form_accountImage}) 
    
    else:
        return HttpResponseRedirect("/")

def organize(word):
        if u"I" in word:
            word = word.replace(u"I",u"ı")
    
        return word.lower()


def mealsAvailable(all_meal):
    if all_meal.count() == 0:
        return False

    return True


def favouriteToggle(request, key):
    if request.user.is_authenticated():
        try:
            meal = Meal.objects.get(id=key)
        except:
            return HttpResponseRedirect("/home/")

        if meal in request.user.profile.favourites.all():
            meal.favourite -= 1 
            meal.save()

            request.user.profile.favourites.remove(meal)
            request.user.save()

            return HttpResponse("Sub")
        else:
            meal.favourite += 1 
            meal.save()

            request.user.profile.favourites.add(meal)
            request.user.save()

            return HttpResponse("Add")
    else:
        return HttpResponseRedirect("/")


def mostFavourites(request):
    if request.user.is_authenticated():
        AllMeal = Meal.objects.filter(favourite__gt=0).order_by("-favourite", "-addingDate")[:3]
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())

        meals_available = mealsAvailable(AllMeal)

        return render(request, "home.html", 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'allFavouriteMeals': allFavouriteMeals,
                       'mostFavouritesPage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

def myFavourites(request):
    if request.user.is_authenticated():
        
        if request.method == "GET":
            remove_mealList =request.GET.getlist('meal')

            for meal_id in remove_mealList:
                try:
                    meal = Meal.objects.get(id=int(meal_id))
                except:
                    ############################
                    # Güzel hata mesajı verdir #
                    ############################   
                    return HttpResponse(u"Buna Yetkiniz Yok!")

                if meal in request.user.profile.favourites.all():
                    request.user.profile.favourites.remove(meal)
                    request.user.save()
                    meal.favourite -= 1 
                    meal.save()
                else:
                    ############################
                    # Güzel hata mesajı verdir #
                    ############################   
                    return HttpResponse(u"Buna Yetkiniz Yok!")

        AllMeal = request.user.profile.favourites.all().order_by("-addingDate")
        currentTime = timezone.localtime(timezone.now())

        meals_available = mealsAvailable(AllMeal)

        return render(request, "home.html", 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'myFavouritesPage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

def myMeals(request):
    if request.user.is_authenticated():

        if request.method == "GET":
            remove_mealList =request.GET.getlist('meal')
            user_mealList = Meal.objects.filter(user=request.user)

            for meal_id in remove_mealList:
                try:
                    meal = Meal.objects.get(id=int(meal_id))
                except:
                    ############################
                    # Güzel hata mesajı verdir #
                    ############################   
                    return HttpResponse(u"Buna Yetkiniz Yok!")

                if meal in user_mealList:
                    material_list = MaterialList.objects.filter(meal=meal)
                    for material in material_list:
                        material.delete()

                    meal.delete()
                else:
                    ############################
                    # Güzel hata mesajı verdir #
                    ############################   
                    return HttpResponse(u"Buna Yetkiniz Yok!")

        AllMeal = Meal.objects.filter(user=request.user).order_by("-addingDate")
        currentTime = timezone.localtime(timezone.now())

        meals_available = mealsAvailable(AllMeal)

        return render(request, "home.html", 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'myMealsPage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

def search(request):
    if request.user.is_authenticated():

        AllMeal = []
        meals_available = True
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())
        
        if request.method == "POST":
            search_method = request.POST.get("search_method")
            search_word = request.POST.get("search_word")

            if search_word != "":
                if search_method == "1" or search_method == "2":
                    
                    AllMeals = Meal.objects.order_by("-addingDate")
            
                    if AllMeals.count() != 0:
                        if search_method == "1":
                            for meal in AllMeals:
                                if organize(meal.name) == organize(search_word):
                                    AllMeal.append(meal)
                        else:
                            for meal in AllMeals:
                                if re.search( organize(search_word), organize(meal.name)):
                                    AllMeal.append(meal)

                elif search_method == "3" or search_method == "4":
                    material_list = MaterialList.objects.all().order_by("-meal__addingDate")

                    if material_list.count() != 0:
                        if search_method == "3":
                            for material_object in material_list:
                                if organize(material_object.material.name) == organize(search_word):
                                    AllMeal.append(material_object.meal)
                        else:
                            for material_object in material_list:
                                if re.search(organize(search_word), organize(material_object.material.name)):
                                    AllMeal.append(material_object.meal)                                     
                else:
                    user_list = User.objects.all()

                    if user_list.count() != 0:
                        if search_method == "5":
                            for user_objects in user_list:
                                if organize(user_objects.get_full_name()) == organize(search_word):
                                    user_meals = Meal.objects.filter(user=user_objects).order_by("-addingDate")

                                    if user_meals.count() != 0:
                                        for meal in user_meals:
                                            AllMeal.append(meal)
                        else:
                            for user_objects in user_list:
                                if re.search(organize(search_word), organize(user_objects.get_full_name())):
                                    user_meals = Meal.objects.filter(user=user_objects).order_by("-addingDate")
                                    
                                    if user_meals.count() != 0:
                                        for meal in user_meals:
                                            AllMeal.append(meal)
        
        if len(AllMeal) == 0:
            meals_available = False

        
        return render(request, "home.html", 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                      'allFavouriteMeals': allFavouriteMeals,
                      'searchPage':True, 'meals_available':meals_available})

    else:
        return HttpResponseRedirect("/")

def home(request):
    if request.user.is_authenticated():

        AllMeal = Meal.objects.order_by("-addingDate")
        meals_available = mealsAvailable(AllMeal)
    
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())

        return render(request, "home.html", 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'allFavouriteMeals': allFavouriteMeals,
                       'homePage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

def showProfile(request, username):
    if request.user.is_authenticated():
        if request.user.username != username:
            try:
                user = User.objects.get(username=username)
                send = Meal.objects.filter(user=user).count()
            except Exception,e:
                return HttpResponseRedirect("/home/")

            if not user.profile.secret_profile:
                return render(request, "userPanel.html", {'user':user, 'send':send})
            else:
                return HttpResponse(u"Gizli")
        else:
            send = Meal.objects.filter(user=request.user).count()
            return render(request, "userPanel.html", {'user':request.user, 'send':send})
    else:
        return HttpResponseRedirect("/")





