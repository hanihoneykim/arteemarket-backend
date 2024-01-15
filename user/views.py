from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import FundingItem
from .serializers import ParticipantSerializer
from .models import Participant


class ParticipantListCreate(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]
    queryset = Participant.objects.all()

    def get(self, request, pk):
        funding_item = FundingItem.objects.get(pk=pk)
        queryset = Participant.objects.filter(funding_item__creator=self.request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        funding_item_id = kwargs.get("pk", None)
        if funding_item_id is None:
            return Response(
                {"detail": "funding_item is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # funding_item_id에 해당하는 FundingItem을 가져오거나 예외 발생
        funding_item = get_object_or_404(FundingItem, id=funding_item_id)

        # FundingItem의 end_date가 오늘 이후인지 확인
        if funding_item.end_date < timezone.now().date():
            return Response(
                {"detail": "신청 가능한 기간이 아닙니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        request.data["user"] = request.user.id
        request.data["funding_item"] = funding_item.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
