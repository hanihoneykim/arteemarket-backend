from rest_framework import serializers
from core.models import SaleItem, FundingItem
from user.serializers import TinyUserSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    creator = TinyUserSerializer(read_only=True)

    class Meta:
        model = SaleItem
        fields = "__all__"
        read_only_fields = ("id",)


class FundingItemSerializer(serializers.ModelSerializer):
    creator = TinyUserSerializer(read_only=True)

    class Meta:
        model = FundingItem
        fields = "__all__"
        read_only_fields = ("id",)
