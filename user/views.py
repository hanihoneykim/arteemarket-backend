from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import FundingItem, SaleItem
from .serializers import ParticipantSerializer, PurchaseSerializer
from .models import Participant, Purchase


class ParticipantListCreate(generics.ListCreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]
    queryset = Participant.objects.all()

    def get(self, request, pk):
        funding_item = get_object_or_404(FundingItem, pk=pk)

        if funding_item.creator != self.request.user:
            raise PermissionDenied("해당 펀딩 상품의 판매자가 아닙니다.")

        queryset = Participant.objects.filter(funding_item=funding_item)
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


class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        funding_item_pk = self.kwargs.get("pk")
        participant_pk = self.kwargs.get("participant_pk")
        participant = get_object_or_404(
            Participant, funding_item__id=funding_item_pk, id=participant_pk
        )
        self.check_object_permissions(self.request, participant)
        return participant

    def get_permissions(self):
        permissions = super().get_permissions()
        funding_item_pk = self.kwargs.get("pk")
        participant_pk = self.kwargs.get("participant_pk")
        participant = get_object_or_404(
            Participant, funding_item__id=funding_item_pk, id=participant_pk
        )

        if participant.funding_item.creator == self.request.user:
            return permissions
        else:
            raise PermissionDenied("권한이 없습니다.")


class PurchaseListCreate(generics.ListCreateAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]
    queryset = Purchase.objects.all()

    def get(self, request, pk):
        sale_item = get_object_or_404(SaleItem, pk=pk)

        if sale_item.creator != self.request.user:
            raise PermissionDenied("해당 상품의 판매자가 아닙니다.")

        queryset = Purchase.objects.filter(sale_item=sale_item)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        sale_item_id = kwargs.get("pk", None)
        sale_item = get_object_or_404(SaleItem, id=sale_item_id)

        request.data["user"] = request.user.id
        request.data["sale_item"] = sale_item.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class PurchaseDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        sale_item_pk = self.kwargs.get("pk")
        purchase_pk = self.kwargs.get("purchase_pk")
        purchase = get_object_or_404(
            Purchase, sale_item__id=sale_item_pk, id=purchase_pk
        )
        self.check_object_permissions(self.request, purchase)
        return purchase

    def get_permissions(self):
        permissions = super().get_permissions()
        sale_item_pk = self.kwargs.get("pk")
        purchase_pk = self.kwargs.get("purchase_pk")
        purchase = get_object_or_404(
            Purchase, sale_item__id=sale_item_pk, id=purchase_pk
        )

        if purchase.sale_item.creator == self.request.user:
            return permissions
        else:
            raise PermissionDenied("권한이 없습니다.")
