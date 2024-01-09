from django.urls import path
from .views import SaleItemListCreate, SaleItemDetail

urlpatterns = [
    path("sale-items", SaleItemListCreate.as_view()),
    path("sale-items/<str:pk>", SaleItemDetail.as_view()),
]
