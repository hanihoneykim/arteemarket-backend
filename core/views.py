from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.permissions import IsCreatorPermission
from rest_framework.parsers import MultiPartParser
from .serializers import (
    SaleItemSerializer,
    FundingItemSerializer,
    MainPageSlideBannerSerializer,
)
from .models import SaleItem, FundingItem, MainPageSlideBanner


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
        my_sale_items_param = request.query_params.get("my_sale_items", "").lower()
        queryset = self.queryset

        if my_sale_items_param == "true" and self.request.user.is_authenticated:
            queryset = queryset.filter(creator=self.request.user)

        search_keyword = self.request.query_params.get("search_keyword", "")
        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

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
        my_funding_items_param = request.query_params.get(
            "my_funding_items", ""
        ).lower()
        queryset = self.queryset

        if my_funding_items_param == "true" and self.request.user.is_authenticated:
            queryset = queryset.filter(creator=self.request.user)

        search_keyword = self.request.query_params.get("search_keyword", "")
        if search_keyword:
            queryset = queryset.filter(title__icontains=search_keyword)

        queryset = queryset.distinct().order_by("-created_at")
        serializer = FundingItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.validated_data["creator"] = self.request.user
        serializer.save()


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


class MainPageSlideBannerListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    permission_classes = [AllowAny]
    serializer_class = MainPageSlideBannerSerializer
    queryset = MainPageSlideBanner.objects.all()
