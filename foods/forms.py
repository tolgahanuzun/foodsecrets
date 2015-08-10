#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import *

from .models import *
from profiles.models import * 
from materials.models import *
import base64


class AddingToMeal(forms.ModelForm):
    name = forms.CharField(label=u"İsim", max_length=100, required=True)
    description = forms.CharField(label=u"Tarif", max_length=10000, 
                                required=True, widget=forms.Textarea)
    meal_kind = forms.ModelChoiceField(label=u"Kind", queryset=MealKind.objects.all(), 
                                       required=True)
    meal_image = forms.ImageField(label=u"Upload Image", required=False)
    meal_hidden = forms.CharField(label=u"Meal Image Src", required=False, 
                                   widget=forms.HiddenInput())

    class Meta:
        model = Meal
        fields = ("name", "description","meal_kind", "meal_image", "meal_hidden")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddingToMeal, self).__init__(*args, **kwargs)

    def organize(self, word):
        if u"I" in word:
            word = word.replace(u"I",u"ı")
    
        return word.lower()

    def totalCalories(self, meal):

        totalCalories = 0
        material_list = MaterialList.objects.filter(meal=meal)

        for material in material_list:
            value = material.amount / float(material.material.amount)
            value *= material.material.calorie 

            totalCalories += value

        return totalCalories

    def clean_name(self):
        user_Allmeals = Meal.objects.filter(user=self.user)
        for user_meal in user_Allmeals:
            if self.organize(self.data.get("name")) == self.organize(user_meal.name):
                raise forms.ValidationError(u'Daha önce bu isimde bir yemek kaydettiniz!')
        
        return self.data.get("name")

    def save(self, commit=True):

        meal = Meal()
        meal.name = self.data.get("name")
        meal.description = self.data.get("description")

        meal_kind = MealKind.objects.get(kind=self.data.get("meal_kind"))
        meal.meal_kind = meal_kind
        meal.user = self.user

        if self.data.get("meal_hidden") != "":
            value = self.data.get("meal_hidden").split(",")
            image_data = base64.b64decode(value[1])
            meal.image = ContentFile(image_data, str(self.user.id) + '.png')

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
    if field.name == 'material':
        return forms.ModelChoiceField(label=u"Malzeme", queryset=Material.objects.all(), 
                                      required=True)
    elif field.name == 'amount':
        return forms.IntegerField(label="Miktar",required=True, min_value=1, initial=1)
    else:
        return field.formfield()
        
MaterialListFormSet = inlineformset_factory(Meal, MaterialList, 
                                            formfield_callback=custom_field_callback,
                                            fields=("material","amount"), can_delete=False, extra=1)



