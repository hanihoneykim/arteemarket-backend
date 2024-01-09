from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.permissions import IsCreatorPermission
from rest_framework.parsers import MultiPartParser
from .serializers import SaleItemSerializer
from .models import SaleItem


class SaleItemListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = SaleItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = SaleItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class SaleItemDetail(generics.RetrieveUpdateDestroyAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = SaleItemSerializer
    permission_classes = [IsCreatorPermission]
    queryset = SaleItem.objects.all()
    lookup_field = "pk"
