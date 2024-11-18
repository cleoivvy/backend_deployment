from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
import uuid
from django.utils.text import slugify


    
    
    
  



class User(AbstractBaseUser, PermissionsMixin):
    
    
    Role = (
        ('admin', 'admin'),
        ('user', 'user')
    )
    
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/', null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=200, choices=Role)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()

    def __str__(self):
        return f"{self.email} -- {self.id}"
    
    
class WeatherUpdate(models.Model):
    
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     country = models.CharField(max_length=300)
     slug = models.SlugField(max_length=300, unique=True, null=True)
     location = models.JSONField(null=True)
     current = models.JSONField(null=True) 
     created_at = models.DateTimeField(auto_now_add=True, null=True)
     updated_at = models.DateTimeField(auto_now=True, null=True)
     
     def __str__(self):
         return f"{self.location.get('name')}"
     
     def save(self, *args, **kwargs):
         self.slug = slugify(self.country)
         super().save(*args, **kwargs)