from rest_framework import serializers
from core.models import SaleItem
from user.serializers import TinyUserSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    creator = TinyUserSerializer()

    class Meta:
        model = SaleItem
        fields = "__all__"
        read_only_fields = ("id",)
