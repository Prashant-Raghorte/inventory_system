from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(
        self, 
        email, 
        password,
        first_name=None,
        last_name=None,
        phone_number=None,
        **extra_fields):
        if not email:
            return ValueError("Email id required!")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password,first_name=first_name,last_name=last_name,phone_number=phone_number,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password,first_name=None,last_name=None,phone_number=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have staff user!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True!')
        return self.create_user(email, password,first_name,last_name,phone_number,**extra_fields)