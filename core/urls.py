from django.urls import path
from .views import SaleItemListCreate

urlpatterns = [
    path("sale-items", SaleItemListCreate.as_view()),
]
