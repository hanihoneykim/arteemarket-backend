from rest_framework import serializers
from core.models import SaleItem


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = "__all__"
        read_only_fields = ("id",)
