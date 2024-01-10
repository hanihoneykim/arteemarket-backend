from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.permissions import IsCreatorPermission
from rest_framework.parsers import MultiPartParser
from .serializers import SaleItemSerializer, FundingItemSerializer
from .models import SaleItem, FundingItem


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
