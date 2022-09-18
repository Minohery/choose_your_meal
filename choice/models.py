from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class dish(models.Model):

    #The dishes in the menu
    choices = models.CharField(max_length=150)

    #Reference of the menu
    ref = models.PositiveIntegerField()
    def __str__(self):
        return self.choices


class User(AbstractUser):
    command = models.BooleanField(default=False)
    choosen = models.PositiveIntegerField(default=1)
    
   
