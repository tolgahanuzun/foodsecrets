#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from profiles.models import Profile

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    email = forms.EmailField(label="Email", required=True)
    phone = forms.CharField(label=u"Phone:", required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "phone", "email", "password1", "password2")

    def clean_email(self):
        data = self.cleaned_data
        user = User.objects.filter(email=data.get('email'))
        if user:
            raise forms.ValidationError(u'Bu mail adresinde bir kullanıcı zaten mevcut.')
    
        return data.get('email')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.save()
            
            user_profile = Profile()
            user_profile.profile = user
            user_profile.phone = self.cleaned_data["phone"]
            user_profile.save()
        
        return user

 
