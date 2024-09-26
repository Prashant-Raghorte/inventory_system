from django.test import TestCase
from user.models import User
from inventory.models import Item
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class ItemViewTests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(password='testpass', email='testuser@example.com')
        cls.token = str(AccessToken.for_user(cls.user))  # Ensure it’s a string
        cls.headers = {'HTTP_AUTHORIZATION': f'Bearer {cls.token}'}

    def test_create_item(self):
        url = reverse('create_item')  # Adjust this to your URL name
        data = {'name': 'Test Item', 'description': 'A test item description'}

        response = self.client.post(url, data, **self.headers)  # Use ** for headers
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    def test_get_item(self):
        item = Item.objects.create(name='Test Item', description='A test item description')
        url = reverse('item_detail', args=[item.id])  # Adjust this to your URL name
        
        response = self.client.get(url, **self.headers)  # Use ** for headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], item.name)

    def test_get_all_items(self):
        Item.objects.create(name='Item 1', description='First item')
        Item.objects.create(name='Item 2', description='Second item')
        url = reverse('create_item')  # Get all items from the same endpoint
        
        response = self.client.get(url, **self.headers)  # Use ** for headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_update_item(self):
        item = Item.objects.create(name='Old Name', description='Old description')
        url = reverse('item_detail', args=[item.id])  # Adjust this to your URL name
        data = {'name': 'New Name', 'description': 'New description'}
        
        response = self.client.put(url, data, **self.headers)  # Use ** for headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, 'New Name')

    def test_partial_update_item(self):
        item = Item.objects.create(name='Old Name', description='Old description')
        url = reverse('item_detail', args=[item.id])  # Adjust this to your URL name
        data = {'name': 'Partially Updated Name'}
        
        response = self.client.patch(url, data, **self.headers)  # Use ** for headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Partially Updated Name')

    def test_delete_item(self):
        item = Item.objects.create(name='Item to delete', description='Delete me')
        url = reverse('item_detail', args=[item.id])  # Adjust this to your URL name
        
        response = self.client.delete(url, **self.headers)  # Use ** for headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Item.objects.count(), 0)

    def test_item_not_found(self):
        url = reverse('item_detail', args=[9999])  # Assuming this ID does not exist
        response = self.client.get(url, **self.headers)  # Use ** for headers
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Item not found')
