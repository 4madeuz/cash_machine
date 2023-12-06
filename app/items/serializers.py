from .models import Item, Receipt, ReceiptItem
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['title', 'price']


class ReceiptsInputSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.IntegerField())


class ReceiptItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReceiptItem
        fields = ['id', 'items_price', 'items_amount']


class ReceiptSerializer(serializers.ModelSerializer):

    receiptitem_set = ReceiptItemSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = ['id', 'total_price', 'created_at', 'receiptitem_set']
