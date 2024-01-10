from rest_framework import serializers
from core.models import SaleItem, FundingItem
from user.models import Participant
from user.serializers import TinyUserSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    creator_nickname = serializers.CharField(source="creator.nickname", read_only=True)
    creator_profile_image = serializers.ImageField(
        source="creator.profile_image", read_only=True
    )

    class Meta:
        model = SaleItem
        fields = "__all__"
        read_only_fields = ("id",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # price 필드를 원하는 형식으로 포매팅
        formatted_price = "{:,.0f}".format(instance.price)
        representation["price"] = formatted_price

        return representation


class FundingItemSerializer(serializers.ModelSerializer):
    creator_nickname = serializers.CharField(source="creator.nickname", read_only=True)
    creator_profile_image = serializers.ImageField(
        source="creator.profile_image", read_only=True
    )
    current_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FundingItem
        fields = "__all__"
        read_only_fields = ("id",)

    def get_current_amount(self, obj):
        participant_count = Participant.objects.filter(funding_item=obj).count()
        current_amount = participant_count * obj.price

        # current_amount를 원하는 형식으로 포매팅
        formatted_current_amount = "{:,.0f}".format(current_amount)
        return formatted_current_amount

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # price 필드를 원하는 형식으로 포매팅
        formatted_price = "{:,.0f}".format(instance.price)
        representation["price"] = formatted_price

        # goal_amount 필드를 원하는 형식으로 포매팅
        formatted_goal_amount = "{:,.0f}".format(instance.goal_amount)
        representation["goal_amount"] = formatted_goal_amount

        return representation
