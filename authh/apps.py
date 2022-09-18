from django.apps import AppConfig
from django.core.signals import request_finished
from django.http import HttpResponse
from django.dispatch import receiver

class AuthhConfig(AppConfig):
    name = 'authh'
    
        
        

