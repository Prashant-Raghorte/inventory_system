from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache

# Create your views here.

import logging
logger = logging.getLogger(__name__)

class ItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete('all_items')
            logger.info(f"New Item added successfully")
            return Response({'message': 'Item created successfully','data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, item_id=None):
        if item_id:
            cached_item = cache.get(f'item_{item_id}')
            if cached_item:
                logger.info(f"Fetching item from cache for this item id {item_id}")
                return Response({'message': 'Item fetch successfully','data':cached_item}, status=status.HTTP_200_OK)

            try:
                item = Item.objects.get(id=item_id)
                serializer = ItemSerializer(item)
                logger.info(f"Item not fetching from cache")
                cache.set(f'item_{item_id}', serializer.data, timeout=60*15)
                return Response({'message': 'Item fetch successfully','data':serializer.data}, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                logger.error(f"Item not found for this item id {item_id}")
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cached_items = cache.get('all_items')
            if cached_items:
                logger.info(f"Fetching item from cache")
                return Response({'message': 'Items List fetch successfully','data':cached_items}, status=status.HTTP_200_OK)

            items = Item.objects.all().order_by('id')
            serializer = ItemSerializer(items, many=True)
            cache.set('all_items', serializer.data, timeout=60*2)
            return Response({'message': 'Items List fetch successfully','data':serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.error(f"Item deleting from cache")
                cache.delete(f'item_{item_id}')
                cache.delete('all_items')
                return Response({'message': 'Item Updated successfully','data':serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f"Item not found for this item id {item_id}")
            return Response({'status':'fail','message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            serializer = ItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.error(f"Item deleting from cache")
                cache.delete(f'item_{item_id}')
                cache.delete('all_items')
                return Response({'message': 'Item partially updated successfully','data':serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            logger.error(f"Item not found for this item id {item_id}")
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            item.delete()
            logger.error(f"Item deleting from cache")
            cache.delete(f'item_{item_id}')
            cache.delete('all_items')
            return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.error(f"Item not found for this item id {item_id}")
            return Response({'status':'fail','message': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)