#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.db.models import Q


from profiles.models import Profile

# Kullanıcı kayıt formu.
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=u"First Name", required=True)
    last_name = forms.CharField(label=u"Last Name", required=True)
    email = forms.EmailField(label=u"Email", required=True)
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

    def previous_values(self):
        data = self.cleaned_data

        values = {
           "first_name":data.get("first_name"),
           "last_name":data.get("last_name"),
           "username":data.get("username"),
           "phone":data.get("phone"),
           "email":data.get("email"),
           "password1":data.get("password1"),
           "password2":data.get("password2")
        }

        return values
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.backend='django.contrib.auth.backends.ModelBackend'
            user.save()
            
            user_profile = Profile()
            user_profile.profile = user
            user_profile.phone = self.cleaned_data["phone"]
            user_profile.save()
        
        return user


# Kullanıcı giriş formu.
class LoginForm(forms.Form):
    username = forms.CharField(label=u"User Name", required=True)
    password = forms.CharField(label=u"Password", widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ("username", "password")

    def is_valid(self):

        valid = super(LoginForm, self).is_valid()

        if not valid:
            return valid

        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if not username or not password:
            return self.cleaned_data

        user = authenticate(username=username,
                            password=password)

        if user:
            self.user = user
        else:
            raise forms.ValidationError(u"Yanlış kullanıcı adı veya şifre!")

        return self.cleaned_data








 
