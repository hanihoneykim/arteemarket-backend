from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.models import FundingItem, SaleItem
from .serializers import ParticipantSerializer, PurchaseSerializer, UserSerializer
from .models import Participant, Purchase, User, AuthToken


class UserSignUp(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        """
        create user using UserSerializer, save hashed password, and return token
        """
        # 기입한 정보가 이미 존재하는 경우 오류 메세지 주기
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                data={"status": "FAILED", "message": "이미 존재하는 이메일입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(nickname=request.data["nickname"]).exists():
            return Response(
                data={"status": "FAILED", "message": "이미 존재하는 닉네임입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token = AuthToken.objects.create(user=user)
        user.set_password(request.data.get("password"))
        user.save()
        return Response(
            {"id": str(user.id), "token": str(token.id)}, status=status.HTTP_201_CREATED
        )


class UserLogin(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            user = User.objects.get(email=email.strip().lower())
        except User.DoesNotExist:
            return Response(
                {"error": "존재하지 않는 유저거나 비밀번호가 맞지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if user.check_password(password):
            token = AuthToken.objects.create(user=user)
            serializer = UserSerializer(user)
            return Response(
                {"token": str(token.id), "info": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "존재하지 않는 유저거나 비밀번호가 맞지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


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
