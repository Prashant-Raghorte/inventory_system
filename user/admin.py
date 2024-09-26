from django.contrib import admin
from user.models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['email','first_name','last_name','phone_number','password','is_staff','is_admin']
    list_display = ['id','email','first_name','last_name','phone_number','is_staff','is_admin', 'created_at','updated_at']
    search_fields = ['email','first_name','last_name']
    list_filter = ['created_at','updated_at']
admin.site.register(User,UserAdmin)
