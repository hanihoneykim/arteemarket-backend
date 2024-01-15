from django.urls import path
from user.views import (
    ParticipantListCreate,
    ParticipantDetail,
    PurchaseListCreate,
    PurchaseDetail,
)
from .views import (
    SaleItemListCreate,
    SaleItemDetail,
    FundingItemListCreate,
    FundingItemDetail,
    MainPageSlideBannerListCreate,
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
    path("sale-items/<str:pk>/purchases", PurchaseListCreate.as_view()),
    path("sale-items/<str:pk>/purchases/<str:purchase_pk>", PurchaseDetail.as_view()),
    path("mainpage-banners", MainPageSlideBannerListCreate.as_view()),
]
