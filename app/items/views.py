from django.conf import settings
from .models import Item, Receipt, ReceiptItem
from .serializers import ItemSerializer, ReceiptsInputSerializer, ReceiptSerializer
from .components import form_pdf_file, form_qr_code
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(
        methods=['post'],
        url_path='cash_machine',
        detail=False,
        serializer_class=ReceiptsInputSerializer,
    )
    def create_check(self, request):
        '''Принимает данные в формате {
            "items": [1, 2, 3], где список items это id модели Item
            Возвращает 404 если в списке только некорректные значения,
            возвращает 201 и ссылку на QR при усипешном выполнении
        '''

        items_ids = request.data.get('items', [])
        items_data = {}

        for item_id in items_ids:
            items_data[item_id] = items_data.get(item_id, 0) + 1

        items = Item.objects.filter(id__in=items_data.keys())

        if not items.exists():
            return Response({"error": "Items not found"}, status=status.HTTP_404_NOT_FOUND)

        receipt_items = []

        receipt = Receipt()

        for item in items:
            item.quantity = items_data[item.id]
            item.items_price = item.quantity * item.price
            receipt_items.append(ReceiptItem(receipt=receipt, item=item, items_price=item.items_price, items_amount=item.quantity))

        total_price = sum(item.items_price for item in items)

        receipt.total_price = total_price
        receipt.save()

        pdf_file_path = form_pdf_file(items, receipt)

        qr_code_path = form_qr_code(pdf_file_path, receipt)

        receipt.save()

        ReceiptItem.objects.bulk_create(receipt_items)

        base_url = settings.BASE_URL
        absolute_url = f"{base_url}/{qr_code_path}"

        return Response({"qr_code_url": absolute_url}, status=status.HTTP_201_CREATED)


class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
