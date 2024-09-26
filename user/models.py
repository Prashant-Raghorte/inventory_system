from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
from user.managers import UserManager
import re

# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    def validate_phone_number(value):
        if re.compile(r"\d{10}").match(value):
            return value
        else:
            raise ValidationError("Phone number entered is incorrect.")

    def validateEmail(email):
        if len(email) > 6:
            if re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email) != None:
                return email
            else:
                raise ValidationError("Email entered is Incorrect.")
        raise ValidationError("Email is Incorrect")
    
    email = models.EmailField(unique=True,validators=[validateEmail])
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    phone_number = models.CharField(max_length=10,validators=[validate_phone_number],blank=True,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name","phone_number"]

    def __str__(self):
        return str(self.email)
