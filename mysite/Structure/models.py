from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin, BaseUserManager
import os
import datetime
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.utils import timezone
# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError("Email not provided")
        if not password: 
            raise ValueError("Password is not provided")
        user = self.model(
            email=self.normalize_email(email),
            
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user( email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models. EmailField(db_index=True, unique= True, max_length=254)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    is_staff = models.BooleanField (default=True) # must needed, otherwise you won't be at
    is_active = models.BooleanField(default=True) # must needed, otherwise you won't be a
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Priority(models.Model):
    class Significance(models.IntegerChoices):
        LOW = 0
        MODERATE = 1
        HIGH = 2
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority_name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    significance = models.IntegerField(choices=Significance.choices)
    image = models.ImageField(upload_to='Structure/files/priorities/covers', default='',blank=True)

class Element(models.Model):
    class Type(models.IntegerChoices):
        MAINTENANCE = 0
        GROWTH = 1
    class Significance(models.IntegerChoices):
        LOW = 0
        MODERATE = 1
        HIGH = 2
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    element_name = models.CharField(max_length = 200)
    description = models.TextField(max_length=500)
    element_type = models.IntegerField(choices=Type.choices)
    
    significance = models.IntegerField(choices=Significance.choices)
    image = models.ImageField(upload_to='Structure/files/elements/covers', default='',blank=True)

class Aspect(models.Model):
    class Significance(models.IntegerChoices):
        LOW = 0
        MODERATE = 1
        HIGH = 2
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    aspect_name = models.CharField(max_length = 200)
    description = models.TextField(max_length=500)
    
    significance = models.IntegerField(choices=Significance.choices)
    image = models.ImageField(upload_to='Structure/files/aspects/covers', default='',blank=True)
    completion = models.BooleanField(default=False)

class Financial_Entity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='Structure/files/financial-entities',default='',blank=True)

class Entity_Aspect(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    active = models.BooleanField(default=True)
    financial_entity = models.ForeignKey(Financial_Entity, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Structure/files/financial-aspects",default="",blank=True)

    
class Entity_Amount(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    amount = models.FloatField()
    entity_aspect = models.ForeignKey(Entity_Aspect, on_delete=models.CASCADE)

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateTimeField()
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=500)
    def upcoming(self):
        return timezone.now()<self.date





