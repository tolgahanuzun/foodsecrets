#-*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django import template
from django.template import Template, Context, RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate

from .models import *
from .forms import *

# Create your views here.


def addFood(request):

    if request.user.is_authenticated():
        if request.method == "POST":
            form_addMeal = AddingToMeal(request.POST)

            if form_addMeal.is_valid():
                meal = form_addMeal.save(commit=False)
                meal.user = request.user
                materialList_formset = MaterialListFormSet(request.POST, instance=meal)

                if materialList_formset.is_valid():
                    meal.save()
                    materialList_formset.save()

                    totalCalories = form_addMeal.totalCalories(meal)
                    meal.totalCalories = totalCalories
                    meal.save() 

                return HttpResponseRedirect("/home/addfood/")
            else:
                return HttpResponse("Hata")
        else:
            form_addMeal = AddingToMeal()
            materialList_formset = MaterialListFormSet()

            return render(request, "addFood.html", {'form_addMeal':form_addMeal,
                                                    'materialList_formset':materialList_formset})
    else:
        return HttpResponseRedirect("/")



