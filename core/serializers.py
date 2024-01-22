from rest_framework import serializers
from core.models import SaleItem, FundingItem, MainPageSlideBanner, Notice, Event
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
    category_name = serializers.CharField(source="category.name", read_only=True)
    current_amount = serializers.SerializerMethodField(read_only=True)
    current_percentage = serializers.SerializerMethodField(read_only=True)

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

    def get_current_percentage(self, obj):
        participant_count = Participant.objects.filter(funding_item=obj).count()
        current_amount = participant_count * obj.price

        # goal_amount가 0이 아닌 경우에만 퍼센티지 계산
        if obj.goal_amount != 0:
            current_percentage = int((current_amount / obj.goal_amount) * 100)
        else:
            current_percentage = 0

        return current_percentage

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # price 필드를 원하는 형식으로 포매팅
        formatted_price = "{:,.0f}".format(instance.price)
        representation["price"] = formatted_price

        # goal_amount 필드를 원하는 형식으로 포매팅
        formatted_goal_amount = "{:,.0f}".format(instance.goal_amount)
        representation["goal_amount"] = formatted_goal_amount

        return representation


class MainPageSlideBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainPageSlideBanner
        fields = "__all__"


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"
