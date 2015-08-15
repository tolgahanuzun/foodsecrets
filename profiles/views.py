#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from endless_pagination.decorators import page_template


from .models import *
from .forms import *
from foods.models import Meal

import re

####### Global Variable #######

# filter function #
meal_kind_buffer = ""
amount_buffer = ""
min_amount_buffer = ""
max_amount_buffer = ""
###################

# search function #
search_method_buffer=""
search_word_buffer=""
###################

###############################

def write(arg):
    print "*****************"
    print arg
    print "*****************"

def tryPage(request):
    return render(request, "follow.html")

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

def accountImage(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form_accountImage = AccountFormImage(request.POST, user=request.user)

            if form_accountImage.is_valid():
                form_accountImage.change();

            return HttpResponseRedirect("/home/account/user/");
    else:
        return HttpResponseRedirect("/");

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


def arrayAvailable(array):
    try:
        if array.count() == 0:
            return False

    except:
        if len(array) == 0:
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

            return HttpResponse("Sub")
        else:
            meal.favourite += 1 
            meal.save()

            request.user.profile.favourites.add(meal)

            return HttpResponse("Add")
    else:
        return HttpResponseRedirect("/")

def followToggle(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/home/")

        control_state1 = user in request.user.profile.following.all()
        control_state2 = user in request.user.profile.send_requests.all()

        if request.user != user:
            
            if user.profile.secret_profile:
                if control_state1:
                    request.user.profile.following.remove(user)
                    user.profile.followers.remove(request.user) 
            
                    return HttpResponse("unfollow-follow_request")
                else:
                    return request_followToggle(request, username)
            else:
                if user in request.user.profile.following.all():
                    request.user.profile.following.remove(user)
                    user.profile.followers.remove(request.user) 
            
                    return HttpResponse("unfollow-follow")
                else:
                    request.user.profile.following.add(user)
                    user.profile.followers.add(request.user) 

                    return HttpResponse("follow-following")

        return HttpResponse("")
    else:
        return HttpResponseRedirect("/")

def request_followToggle(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/home/")

        if request.user != user:
            if user in request.user.profile.send_requests.all():
                request.user.profile.send_requests.remove(user)
                user.profile.received_requests.remove(request.user)

                return HttpResponse("cancel_request-follow_request")
            else:
                request.user.profile.send_requests.add(user)
                user.profile.received_requests.add(request.user)
                
                return HttpResponse("follow_request-cancel_request")

        return HttpResponse("")

    else:
        return HttpResponseRedirect("/")

def acceptRequest(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/home/")

        if request.user != user:
            request.user.profile.followers.add(user)
            user.profile.following.add(request.user)

            request.user.profile.received_requests.remove(user)
            user.profile.send_requests.remove(request.user)

        return HttpResponse("")

    else:
        return HttpResponseRedirect("/")

def cancelRequest(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/home/")

        if request.user != user:
            request.user.profile.received_requests.remove(user)
            user.profile.send_requests.remove(request.user)

        return HttpResponse("")

    else:
        return HttpResponseRedirect("/")

def blockUserToggle(request, username):
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponseRedirect("/home/")

        if request.user != user:
            if user in request.user.profile.myBlocked.all():
                request.user.profile.myBlocked.remove(user)
                user.profile.blockedMe.remove(request.user)

                return HttpResponse("unblock-block")
            else:
                request.user.profile.following.remove(user)
                request.user.profile.followers.remove(user)
                user.profile.following.remove(request.user)
                user.profile.followers.remove(request.user)
                request.user.profile.send_requests.remove(user)
                request.user.profile.received_requests.remove(user)
                user.profile.send_requests.remove(request.user)
                user.profile.received_requests.remove(request.user)

                # Yemekleri favorilere ekleme olayı olabilir onlarda silinmeli.

                request.user.profile.myBlocked.add(user)
                user.profile.blockedMe.add(request.user)

                return HttpResponse("block-unblock")


    else:
        return HttpResponseRedirect("")


@page_template("../templates/pagination.html")
def friendRequests(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():
        AllUsers = request.user.profile.received_requests.all()
        requests_available = arrayAvailable(AllUsers)

        return render(request, template, 
                      {'AllUsers':AllUsers, 'friendRequestsPage':True,
                       'requests_available':requests_available }) 

    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def mostFavourites(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():
        AllMeal = Meal.objects.filter(favourite__gt=0).order_by("-favourite", "-addingDate")[:5]
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())

        meals_available = arrayAvailable(AllMeal)

        return render(request, template, 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'allFavouriteMeals': allFavouriteMeals,
                       'mostFavouritesPage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def myFavourites(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():
        
        if request.method == "GET":
            remove_mealList =request.GET.getlist('meal')

            for meal_id in remove_mealList:
                try:
                    meal = Meal.objects.get(id=int(meal_id))

                    if meal in request.user.profile.favourites.all():
                        request.user.profile.favourites.remove(meal)
                        request.user.save()
                        meal.favourite -= 1 
                        meal.save()
                    else:
                        # Güzel bir hata mesajı verdir.
                        pass

                except:
                    # Güzel bir hata mesajı verdir.
                    pass

        AllMeal = request.user.profile.favourites.all().order_by("-addingDate")
        currentTime = timezone.localtime(timezone.now())

        meals_available = arrayAvailable(AllMeal)

        return render(request, template, 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'myFavouritesPage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def myMeals(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        if request.method == "GET":
            remove_mealList =request.GET.getlist('meal')
            user_mealList = Meal.objects.filter(user=request.user)

            for meal_id in remove_mealList:
                try:
                    meal = Meal.objects.get(id=int(meal_id))
                    
                    if meal in user_mealList:
                        material_list = MaterialList.objects.filter(meal=meal)
                        for material in material_list:
                            material.delete()

                        meal.delete()
                    else:
                        # Güzel bir hata mesajı verdir.
                        pass

                except:
                    # Güzel bir hata mesajı verdir.
                    pass

        AllMeal = Meal.objects.filter(user=request.user).order_by("-addingDate")
        currentTime = timezone.localtime(timezone.now())

        meals_available = arrayAvailable(AllMeal)

        return render(request, template, 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'myMealsPage':True, 'meals_available':meals_available })
    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def myFollowers(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        AllUsers = request.user.profile.followers.all()
        users_available = arrayAvailable(AllUsers)

        return render(request, template, 
                      {'AllUsers':AllUsers, 'profileFollowPage':True,
                       'profileFollowersPage':True,
                       'users_available':users_available})

    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def myFollowing(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        AllUsers = request.user.profile.following.all()
        users_available = arrayAvailable(AllUsers)

        return render(request, template, 
                      {'AllUsers':AllUsers, 'profileFollowPage':True,
                       'profileFollowingPage':True,
                       'users_available':users_available})
    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def filter(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        global meal_kind_buffer
        global amount_buffer
        global min_amount_buffer
        global max_amount_buffer
        
        if request.method == "POST":
            meal_kind_buffer = meal_kind = request.POST.getlist("kind_select")
            amount_buffer = amount = request.POST.get("amount")
            min_amount_buffer = min_amount = amount.split("-")[0]
            max_amount_buffer = max_amount = amount.split("-")[1]
        else:
            meal_kind = meal_kind_buffer
            amount = amount_buffer
            min_amount = min_amount_buffer
            max_amount = max_amount_buffer

        following_list = request.user.profile.following.all()

        if len(meal_kind) != 0:
            AllMeal = Meal.objects.filter(Q(user__profile__secret_profile=False) |
                                          Q(user__in=following_list) | 
                                          Q(user=request.user)).filter(
                                          Q(totalCalories__gte=min_amount) & 
                                          Q(totalCalories__lte=max_amount) & 
                                          Q(meal_kind__kind__in=meal_kind)).order_by("-addingDate")
        else:
            AllMeal = Meal.objects.filter(Q(user__profile__secret_profile=False) |
                                          Q(user__in=following_list) | 
                                          Q(user=request.user)).filter(
                                          Q(totalCalories__gte=min_amount) & 
                                          Q(totalCalories__lte=max_amount)).order_by("-addingDate")
        
        meals_available = arrayAvailable(AllMeal)
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())

        return render(request, template, 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'allFavouriteMeals': allFavouriteMeals,
                       'meals_available':meals_available, 'filterPage':True})


    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def search(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        global search_method_buffer
        global search_word_buffer

        if request.method == "POST":
            search_method_buffer = search_method = request.POST.get("search_method")
            search_word_buffer = search_word = request.POST.get("search_word")
        else:
            search_method = search_method_buffer
            search_word = search_word_buffer

        AllUsers = [] # search users
        AllMeal = []
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())
        following_list = request.user.profile.following.all()

        if search_word != "":
            if search_method == "1" or search_method == "2":
                
                AllMeals = Meal.objects.filter(Q(user__profile__secret_profile=False) |
                                               Q(user__in=following_list) | 
                                               Q(user=request.user)).order_by("-addingDate")
        
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
                material_list = MaterialList.objects.filter(Q(meal__user__profile__secret_profile=False) |
                                                            Q(meal__user__in=following_list) | 
                                                            Q(meal__user=request.user)).order_by("-meal__addingDate")

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
                                AllUsers.append(user_objects)

                    else:
                        for user_objects in user_list:
                            if re.search(organize(search_word), organize(user_objects.get_full_name())):
                                AllUsers.append(user_objects)
                                

        if search_method == "5" or search_method == "6":
            users_available = arrayAvailable(AllUsers)
            return render(request, template, 
                      {'AllUsers':AllUsers, 'profileFollowPage':True,
                       'users_available':users_available})
        else:
            meals_available = arrayAvailable(AllMeal)

            return render(request, template, 
                           {'AllMeal':AllMeal, 'currentTime':currentTime,
                            'allFavouriteMeals': allFavouriteMeals,
                            'searchPage':True, 'meals_available':meals_available})

    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def home(request, template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():

        following_list = request.user.profile.following.all()
        AllMeal = Meal.objects.filter( Q(user__in=following_list) | Q(user=request.user) ).order_by("-addingDate")
        meals_available = arrayAvailable(AllMeal)
    
        allFavouriteMeals = request.user.profile.favourites.all()
        currentTime = timezone.localtime(timezone.now())

        return render(request, template, 
                      {'AllMeal':AllMeal, 'currentTime':currentTime,
                       'allFavouriteMeals': allFavouriteMeals,
                       'homePage':True, 'meals_available':meals_available})
    else:
        return HttpResponseRedirect("/")

@page_template("../templates/pagination.html")
def showProfile(request, username, mod="meals" ,template="../templates/home.html", extra_context=None):
    if request.user.is_authenticated():
        
        other_profilePageFav = False
        other_profilePageMeals = False
        other_profilePageMostFav = False
        profileFollowPage = False

        try:
            user = User.objects.get(username=username)
            
            if mod == "meals" or mod == "favourites" or mod == "mostfavourites":
                if mod == "meals":
                    AllMeal = Meal.objects.filter(user=user).order_by("-addingDate")
                    other_profilePageMeals = True
                elif mod == "favourites":
                    AllMeal = user.profile.favourites.all()
                    other_profilePageFav = True
                else:   # mod == mostfavourites
                    AllMeal = Meal.objects.filter(favourite__gt=0).order_by("-favourite", "-addingDate")[:5]
                    other_profilePageMostFav = True
        
                meals_available = arrayAvailable(AllMeal)
                allFavouriteMeals = request.user.profile.favourites.all()
                currentTime = timezone.localtime(timezone.now())
        
            else: # mod == following or mod == followers
                if mod == "followers":
                    AllUsers = user.profile.followers.all()
                    profileFollowPage = True
                else: #mod == following
                    AllUsers = user.profile.following.all()
                    profileFollowPage = True

                users_available = arrayAvailable(AllUsers)

        except Exception,e:
            return HttpResponseRedirect("/home/")

        if mod == "meals" or mod == "favourites" or mod == "mostfavourites":
            return render(request, template, 
                            {'AllMeal':AllMeal, 'currentTime':currentTime,
                             'allFavouriteMeals': allFavouriteMeals, 'otherUser':user,
                             'other_profilePage':True,'meals_available':meals_available,
                             'other_profilePageFav':other_profilePageFav,
                             'other_profilePageMeals':other_profilePageMeals,
                             'other_profilePageMostFav':other_profilePageMostFav })
        else: # mod == following or mod == followers
            return render(request, template, 
                            {'AllUsers':AllUsers, 'otherUser':user,
                             'other_profilePage':True,
                             'profileFollowPage':profileFollowPage,
                             'users_available':users_available })     
    
    else:
        return HttpResponseRedirect("/")


