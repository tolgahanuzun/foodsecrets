#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http import *


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
        user = User.objects.exists(email=data.get('email'))
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

class AccountFormUser(forms.Form):
    first_name = forms.CharField(label=u"First Name", required=True)
    last_name = forms.CharField(label=u"Last Name", required=True)
    email = forms.EmailField(label=u"Email", required=True)
    phone = forms.CharField(label=u"Phone:", required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountFormUser, self).__init__(*args, **kwargs)


    def change(self):

        user_profile = Profile.objects.get(profile=self.user)
        data = self.cleaned_data

        self.user.first_name = data.get("first_name")
        self.user.last_name = data.get("last_name")
        self.user.email = data.get("email")
        self.user.save()

        user_profile.profile = self.user
        user_profile.phone = data.get("phone")
        user_profile.save()

        return self.user



class AccountFormPassword(forms.Form):
    currentPassword = forms.CharField(label=u"Current Password", widget=forms.PasswordInput, required=True)
    newPassword = forms.CharField(label=u"New Password", widget=forms.PasswordInput, required=True)
    confirm_newPassword = forms.CharField(label=u"Confirm New Password", widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AccountFormPassword, self).__init__(*args, **kwargs)

    def clean_currentPassword(self):
        currentPassword = self.cleaned_data.get("currentPassword")

        if not self.user.check_password(currentPassword):
            raise forms.ValidationError(u"Mevcut şifre hatalı!")

        return True


    def clean_confirm_newPassword(self):
        newPassword = self.cleaned_data.get("newPassword")
        confirm_newPassword = self.cleaned_data.get("confirm_newPassword")

        if newPassword != confirm_newPassword:
            raise forms.ValidationError(u"Yeni girilen şifreler uyuşmuyor.")
        
        return True

    ##############################################
    #   Aynı şifre girildiğinde hata verilecek   #
    ##############################################

    #def clean_newPassword(self):
    #    currentPassword = self.cleaned_data.get("currentPassword")
    #    newPassword = self.cleaned_data.get("newPassword")

    #    if currentPassword == newPassword:
    #        raise forms.ValidationError(u"Yeni girdiğiniz şifre mevcut şifrenizle aynı.") 
    #       
    #    return True


    def change(self):        
        
        self.user.set_password(self.cleaned_data.get("newPassword"))
        self.user.save()

        self.user = authenticate(username=self.user.username,
                                 password=self.cleaned_data.get("newPassword"))

        return self.cleaned_data

    class Meta:
        fields = ("currentPassword", "newPassword", "confirm_newPassword")

    

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








 
