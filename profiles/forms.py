#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.core.files.base import ContentFile
from django.db.models import Q
from django.http import *


from profiles.models import Profile

import base64

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
           "password2":data.get("password2"),
           "vehicle":data.get("vehicle")
        }

        return values
    
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        if commit:
            user.backend='django.contrib.auth.backends.ModelBackend'
            user.save()
            
            user_profile = Profile()
            user_profile.user = user
            user_profile.phone = self.cleaned_data["phone"]
            user_profile.save()
        
        return user


class AccountFormImage(forms.Form):
    change_image = forms.ImageField(label=u"Change Profile Image", required=False)
    hidden_field = forms.CharField(label=u"Profile Src", required=False, 
                                   widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountFormImage, self).__init__(*args, **kwargs)

 
    def change(self):
        data = self.cleaned_data

        if data.get("hidden_field") != "":
            value = self.data.get("hidden_field").split(",")
            
            image_data = base64.b64decode(value[1])

            user_profile = Profile.objects.get(user=self.user) 
            user_profile.image = ContentFile(image_data, str(self.user.id) + '.png')
            user_profile.save()

        return self.user


class AccountFormUser(forms.Form):
    first_name = forms.CharField(label=u"First Name", required=True)
    last_name = forms.CharField(label=u"Last Name", required=True)
    email = forms.EmailField(label=u"Email", required=True)
    phone = forms.CharField(label=u"Phone:", required=False)
    secret_profile = forms.BooleanField(label=u"Secret Profile", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountFormUser, self).__init__(*args, **kwargs)
    
    def clean_email(self):
        
        try:
            user = User.objects.get(email=self.cleaned_data.get('email'))   
        except:
            return self.cleaned_data.get("email")

        if user != self.user:
            raise forms.ValidationError(u'Bu mail adresinde bir kullanıcı zaten mevcut.')
        else:
            return self.cleaned_data.get("email")

    def change(self):

        user_profile = Profile.objects.get(user=self.user)
        data = self.cleaned_data

        self.user.first_name = data.get("first_name")
        self.user.last_name = data.get("last_name")
        self.user.email = data.get("email")
        self.user.save()

        user_profile.user = self.user
        user_profile.phone = data.get("phone")
        user_profile.secret_profile = data.get("secret_profile")
        user_profile.save()

        return self.user



class AccountFormPassword(forms.Form):
    currentPassword = forms.CharField(label=u"Current Password", widget=forms.PasswordInput, required=True)
    newPassword = forms.CharField(label=u"New Password", widget=forms.PasswordInput, required=True)
    confirm_newPassword = forms.CharField(label=u"Confirm New Password", widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ("currentPassword", "newPassword", "confirm_newPassword")

    def __init__(self, *args, **kwargs):
        self.currentPassword = 0
        self.newPassword = 0
        self.confirm_newPassword = 0
        self.error = 0
        
        self.user = kwargs.pop('user', None)
        super(AccountFormPassword, self).__init__(*args, **kwargs)

    def setValue(self):

        self.currentPassword = self.data.get("currentPassword", None)
        self.newPassword = self.data.get("newPassword", None)
        self.confirm_newPassword = self.data.get("confirm_newPassword", None)


    def clean_currentPassword(self):

        if not self.user.check_password(self.currentPassword):
            self.error = 1
            raise forms.ValidationError(u"Mevcut şifre hatalı !")

        return self.currentPassword

    def clean_newPassword(self):

        if self.error == 1:
            return self.newPassword
        else:
            if self.currentPassword == self.newPassword:
                raise forms.ValidationError(u"Yeni girdiğiniz şifre mevcut şifreniz ile aynı !")

            return self.newPassword 

    def clean_confirm_newPassword(self):

        if self.error == 1:
            return self.confirm_newPassword
        else:
            if self.newPassword != self.confirm_newPassword:
                raise forms.ValidationError(u"Yeni girilen şifreler uyuşmuyor !")

            return self.confirm_newPassword

    def change(self):        
        
        self.user.set_password(self.cleaned_data.get("newPassword"))
        self.user.save()

        self.user = authenticate(username=self.user.username,
                                 password=self.cleaned_data.get("newPassword"))

        return self.cleaned_data
 

# Kullanıcı giriş formu.
class LoginForm(forms.Form):
    username = forms.CharField(label=u"User Name", required=True)
    password = forms.CharField(label=u"Password", widget=forms.PasswordInput, required=True)

    class Meta:
        fields = ("username", "password")

    def clean(self):

        clean = super(LoginForm, self).clean()

        if not clean:
            return clean

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








 
