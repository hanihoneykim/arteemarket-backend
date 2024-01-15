from rest_framework import serializers
from .models import User, Participant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "profile_image",
        )


class ParticipantSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    user_profile_image = serializers.ImageField(
        source="user.profile_image", read_only=True
    )

    class Meta:
        model = Participant
        fields = "__all__"
        read_only_fields = ("id",)
