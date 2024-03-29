from django.urls import path
from .views import (
    UserSignUp,
    UserLogin,
    MyProfileDetail,
    SocialAuthentication,
    UserLogout,
    MyParticipantList,
    MyPurchaseList,
    MyParticipantDetail,
    MyPurchaseDetail,
)

urlpatterns = [
    path("signup", UserSignUp.as_view()),
    path("login", UserLogin.as_view()),
    path("logout", UserLogout.as_view()),
    path("myprofile", MyProfileDetail.as_view()),
    path("my-participants", MyParticipantList.as_view()),
    path("my-participants/<str:pk>", MyParticipantDetail.as_view()),
    path("my-purchases", MyPurchaseList.as_view()),
    path("my-purchases/<str:pk>", MyPurchaseDetail.as_view()),
    path("social/<str:provider>", SocialAuthentication.as_view()),
]
