from django.urls import path
from user.views import ParticipantListCreate, ParticipantDetail
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
    path("funding-items/<str:pk>/participants", ParticipantListCreate.as_view()),
    path(
        "funding-items/<str:pk>/participants/<str:participant_pk>",
        ParticipantDetail.as_view(),
    ),
]
