from django.urls import path
from .views import ItemView

urlpatterns = [
    path('items/', ItemView.as_view(), name='create_item'),
    path('items/<int:item_id>/', ItemView.as_view(), name='item_detail'),
]
