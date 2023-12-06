from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ReceiptViewSet

app_name = 'items'

router = DefaultRouter()

router.register('items', ItemViewSet, basename='items')
router.register('receipts', ReceiptViewSet, basename='receipts')

urlpatterns = [
    path('v1/', include(router.urls)),
]
