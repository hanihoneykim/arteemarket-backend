from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from config.permissions import IsCreatorPermission
from rest_framework.parsers import MultiPartParser
from .serializers import (
    SaleItemSerializer,
    FundingItemSerializer,
    MainPageSlideBannerSerializer,
    NoticeSerializer,
    EventSerializer,
)
from .models import SaleItem, FundingItem, MainPageSlideBanner, Notice, Event


class SaleItemListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]

        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        category_param = request.query_params.get("category", "").lower()
        queryset = self.queryset

        # 카테고리 필터링
        if category_param:
            queryset = queryset.filter(category=category_param)

        queryset = queryset.distinct().order_by("-created_at")
        serializer = SaleItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SaleItemDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == ["PUT", "PATCH", "DELETE"]:
            return [IsCreatorPermission()]

        return super().get_permissions()


class SaleItemSearch(generics.ListCreateAPIView):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        search_keyword = self.request.query_params.get("search_keyword", "")
        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        queryset = queryset.distinct().order_by("-created_at")
        serializer = SaleItemSerializer(queryset, many=True)
        return Response(serializer.data)


class MySaleItem(generics.ListCreateAPIView):
    serializer_class = SaleItemSerializer
    queryset = SaleItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SaleItem.objects.filter(creator=self.request.user)


class FundingItemListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = FundingItemSerializer
    queryset = FundingItem.objects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAuthenticated()]

        return super().get_permissions()

    def get(self, request, *args, **kwargs):
        recent_param = request.query_params.get("recent", "").lower()
        category_param = request.query_params.get("category", "").lower()
        queryset = self.queryset

        # 카테고리 필터링
        if category_param:
            queryset = queryset.filter(category=category_param)

        queryset = queryset.distinct().order_by("-created_at")

        # 최신 작성 8개
        if recent_param == "true":
            queryset = queryset[:8]

        serializer = FundingItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.validated_data["creator"] = self.request.user
        serializer.save()


class FundingItemSearch(generics.ListCreateAPIView):
    serializer_class = FundingItemSerializer
    queryset = FundingItem.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset
        search_keyword = self.request.query_params.get("search_keyword", "")
        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        queryset = queryset.distinct().order_by("-created_at")
        serializer = FundingItemSerializer(queryset, many=True)
        return Response(serializer.data)


class FundingItemDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = FundingItemSerializer
    queryset = FundingItem.objects.all()
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == ["PUT", "PATCH", "DELETE"]:
            return [IsCreatorPermission()]

        return super().get_permissions()


class MyFundingItem(generics.ListCreateAPIView):
    serializer_class = FundingItemSerializer
    queryset = FundingItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FundingItem.objects.filter(creator=self.request.user)


class MainPageSlideBannerListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    serializer_class = MainPageSlideBannerSerializer
    queryset = MainPageSlideBanner.objects.all()


class NoticeListCreate(generics.ListCreateAPIView):
    queryset = Notice.objects.all().order_by("-created_at")
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return super().get_permissions()


class NoticeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoticeSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]

        return super().get_permissions()

    def get_queryset(self):
        return Notice.objects.all()


class EventListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == "POST":
            return [IsAdminUser()]

        return super().get_permissions()


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = EventSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        elif self.request.method == ["PUT", "PATCH", "DELETE"]:
            return [IsAdminUser()]

        return super().get_permissions()

    def get_queryset(self):
        return Event.objects.all()
