from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser
from .serializers import SaleItemSerializer
from .models import SaleItem


class SaleItemListCreate(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser]
    serializer_class = SaleItemSerializer
    permission_classes = [AllowAny]
    queryset = SaleItem.objects.all()
