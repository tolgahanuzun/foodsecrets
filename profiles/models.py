#-*- coding: utf-8 -*-

from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Profile(models.Model):
    profile = models.OneToOneField(User,verbose_name="Kullanıcı")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=15,validators=[phone_regex], blank=True) # validators should be a list
