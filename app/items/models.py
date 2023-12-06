from django.db import models
from django.core.validators import MinValueValidator


class Item(models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0),])


class Receipt(models.Model):
    total_price = models.FloatField(validators=[MinValueValidator(0),])
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='media/', blank=True, null=True)
    items = models.ManyToManyField(Item, through='ReceiptItem')


class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    items_price = models.FloatField(validators=[MinValueValidator(0),])
    items_amount = models.IntegerField(validators=[MinValueValidator(1),])
