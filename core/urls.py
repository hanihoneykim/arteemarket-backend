from django.urls import path
from .views import (
    SaleItemListCreate,
    SaleItemDetail,
    FundingItemListCreate,
    FundingItemDetail,
)

urlpatterns = [
    path("sale-items", SaleItemListCreate.as_view()),
    path("sale-items/<str:pk>", SaleItemDetail.as_view()),
    path("funding-items", FundingItemListCreate.as_view()),
    path("funding-items/<str:pk>", FundingItemDetail.as_view()),
]
