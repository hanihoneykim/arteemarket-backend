from rest_framework import serializers
from .models import User, Participant, Purchase
from core.serializers import TinyFundingItemSerializer, TinySaleItemSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "profile_image",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "nickname",
            "profile_image",
            "name",
            "phone_number",
        )
        read_only_fields = (
            "id",
            "email",
        )


class EditPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            "password",
            "old_password",
            "new_password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class ParticipantSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    user_profile_image = serializers.ImageField(
        source="user.profile_image", read_only=True
    )

    class Meta:
        model = Participant
        fields = "__all__"
        read_only_fields = ("id",)


class PurchaseSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    user_profile_image = serializers.ImageField(
        source="user.profile_image", read_only=True
    )

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("id",)


class MyParticipantSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    funding_item = TinyFundingItemSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = "__all__"
        read_only_fields = ("id",)


class MyPurchaseSerializer(serializers.ModelSerializer):
    sale_item = TinySaleItemSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ("id",)
