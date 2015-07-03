from django.contrib import admin

# Register your models here.

from .models import *
from .forms import *

class MaterialListInline(admin.TabularInline):
    model = MaterialList
    extra=3

class NewFood(admin.ModelAdmin):
    inlines = [MaterialListInline]

admin.site.register(Food, NewFood)
admin.site.register(FoodKind)