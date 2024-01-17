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
    FundingItemSearch,
    SaleItemSearch,
    MySaleItem,
    MyFundingItem,
)

urlpatterns = [
    path("sale-items", SaleItemListCreate.as_view()),
    path("sale-items/search", SaleItemSearch.as_view()),
    path("sale-items/myitems", MySaleItem.as_view()),
    path("sale-items/<str:pk>", SaleItemDetail.as_view()),
    path("funding-items", FundingItemListCreate.as_view()),
    path("funding-items/search", FundingItemSearch.as_view()),
    path("funding-items/myitems", MyFundingItem.as_view()),
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
