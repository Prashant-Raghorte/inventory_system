from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    fields = ['name','description','quantity']
    list_display = ['id','name','description','quantity']
    search_fields = ['name','description','quantity']
admin.site.register(Item,ItemAdmin)


# class Item(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField()
#     quantity = models.IntegerField(default=0)

#     def __str__(self):
#         return self.name