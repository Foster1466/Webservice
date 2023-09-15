from rest_framework import serializers
from .models import *

# Serializers for our models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['shortDescription', 'price']

# Serializer for the 'Receipt' model, including a nested 'ItemSerializer' for 'items'
class ReceiptSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = ['retailer', 'purchaseDate', 'purchaseTime', 'total', 'items']