#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class userAdd_form(forms.Form):
    username = forms.CharField(label=u"KULLANICI ADI:")
    first_name = forms.CharField(label=u"AD:")
    last_name = forms.CharField(label=u"SOYAD:")
    email = forms.EmailField(label=u"E-Mail:")
    phone = forms.CharField(required=False,label=u"Telefon")
    password = forms.CharField(label=u"Şifre")
    password_again = forms.CharField(label=u"Şifre(Tekrar)")

    def clean_e_mail(self):
        e_mail_adress = self.cleaned_data['e_mail']
        if '@' in e_mail_adress:
            (user, area) = e_mail_adress.split('@')
            if user in ('root', 'admin', 'administator'):
                raise forms.ValidationError(u'Bu adres geçersizdir.')
    
        return e_mail_adress

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(label=u"Ad:")
    last_name = forms.CharField(label=u"Soyad:")
    phone = forms.CharField(required=False,label=u"Telefon")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")

 
