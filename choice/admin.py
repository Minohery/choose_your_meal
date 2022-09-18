from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.

def has_ordered(modeladmin, request, queryset):

    #Tell that the user has ordered
    queryset.update(command=True)
has_ordered.short_description = "Has ordered"

def has_not_ordered(modeladmin, request, queryset):

    #Tell that the user has not ordered
    queryset.update(command=False)
has_not_ordered.short_description = "Has not ordered"


class UserAdmi(UserAdmin):
    list_display = ('username', 'command', 'choosen')
    actions = [has_ordered, has_not_ordered]



admin.site.register(User, UserAdmi)
admin.site.register(models.dish)




