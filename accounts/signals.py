import random 
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
import time 
from django.utils import timezone
from .models import *
import hashlib
import os

User = get_user_model()


@receiver(post_save, sender=User)
def welcome_user_mail(sender, instance, created, **kwargs):
    
    if created:
        if instance.role == 'user':
            subject = "openapi welcomes you"
            message = f"Dear {instance.first_name}, welcome to my system. My name is Cleon. I am here to help you navigate the world as a woman. if you have any question, please let me know"
            
            print("sending mail")
            time.sleep(5)
            print("mail sent")
            
            print(f"""
                  subject: {subject}
                  message: {message}
                  """)
            
        else:
            print("Admin created")
            print(f""""
                  subject: openapi welcomes Admin
                  message: Dear Admin, My name is Cleon. I am here to help you navigate the world as a woman. if you have any question, please let me know
                  """)