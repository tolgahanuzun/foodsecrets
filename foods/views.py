#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

def addMeal(request):

    if request.user.is_authenticated():
        if request.method == "POST":
            form_addMeal = AddingToMeal(request.POST, user=request.user)
            materialList_formset = MaterialListFormSet(request.POST)
            
        
            if form_addMeal.is_valid() and materialList_formset.is_valid():
                meal = form_addMeal.save(commit=False)
                meal.user = request.user
                materialList_formset = MaterialListFormSet(request.POST, instance=meal)

                if materialList_formset.is_valid():
                    meal.save()
                    materialList_formset.save()

                    totalCalories = form_addMeal.totalCalories(meal)
                    meal.totalCalories = totalCalories
                    meal.save() 

                return HttpResponseRedirect("/home/addmeal/")
            else:
                return render(request, "addFood.html", {'form_addMeal':form_addMeal,
                                                        'materialList_formset':materialList_formset})
        else:
            form_addMeal = AddingToMeal()
            materialList_formset = MaterialListFormSet()

            return render(request, "addFood.html", {'form_addMeal':form_addMeal,
                                                    'materialList_formset':materialList_formset})
    else:
        return HttpResponseRedirect("/")


def showMeal(request, key=None):
    if request.user.is_authenticated():
        try:
            meal = Meal.objects.get(id=key)
            materialList = MaterialList.objects.filter(meal=meal)
        except:
            return  HttpResponseRedirect("/home/")

        return render(request, 'meal.html', {'meal':meal, 'materialList':materialList})
    else:
        return HttpResponseRedirect("/")





