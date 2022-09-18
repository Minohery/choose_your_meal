from django.db import models

# Create your models here.

from choice.models import User




class confirmation_code(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE)
    ref=models.PositiveIntegerField(default=1)
    num=models.PositiveIntegerField()
    new_password=models.CharField(max_length=9)
    qualified=models.BooleanField(default=False)
    confirm=models.BooleanField(default=False)
    def __str__(self):
        return self.new_password

class has_perm_success(models.Model):
    name=models.ForeignKey(User, on_delete=models.CASCADE)
    ref=models.PositiveIntegerField(default=1)
    permission = models.BooleanField(default=False)
