#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.db.models import Q
from django.http import *

from .models import *
from profiles.models import * 
from materials.models import *


class AddingToMeal(forms.ModelForm):
    name = forms.CharField(label=u"İsim", max_length=100, required=True)
    description = forms.CharField(label=u"Tarif", max_length=1000, 
                                required=True, widget=forms.Textarea)
    meal_kind = forms.ModelChoiceField(label=u"Kind", queryset=MealKind.objects.all(), required=True)

    class Meta:
        model = Meal
        fields = ("name", "description","meal_kind")

    def totalCalories(self, meal):

        totalCalories = 0
        material_list = MaterialList.objects.filter(meal=meal)

        for material in material_list:
            value = material.amount / float(material.material.amount)
            value *= material.material.calorie 

            totalCalories += value

        return totalCalories


    def save(self, commit=True):
        meal = super(AddingToMeal, self).save(commit=False)

        if commit:
            meal.name = data.get("name")
            meal.description = data.get("description")
            meal.meal_kind = data.get("food_kind")
            meal.save()
 
        return meal

def custom_field_callback(field):
    #if field.name == 'name':
    #    return forms.CharField(label=u"İsim", max_length=100, required=True)
    #elif field.name == 'description':
    #    return forms.CharField(label=u"Tarif", max_length=1000, 
    #                            required=True, widget=forms.Textarea)
    #elif field.name == 'food_kind':
    #    return forms.ModelChoiceField(label=u"Kind", queryset=FoodKind.objects.all(), 
    #                                  required=True)
    #elif field.name == 'material':
    #    return forms.ModelChoiceField(label=u"Malzeme", queryset=Material.objects.all(), 
    #                                  required=True)
    if field.name == 'amount':
        return forms.IntegerField(label="Miktar",required=True, min_value=1, initial=1)
    else:
        return field.formfield()
        
MaterialListFormSet = inlineformset_factory(Meal, MaterialList, 
                                            formfield_callback=custom_field_callback,
                                            fields=("material","amount"), can_delete=False, extra=1)



