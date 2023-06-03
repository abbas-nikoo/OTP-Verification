import redis
from random import randint

from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserLoginsSerializers, VerifyOtpSerializer, PostSerializers
from .permissions import IsOwnerOrReadeOnly
from .models import PostModel
from .tasks import send_sms

redis_code = redis.Redis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
random_code = str(randint(100000, 999999))


class UserLogin(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginsSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        otp1 = redis_code.get(phone)
        if otp1 is None:
            send_sms.apply_async(args=[phone, random_code])
            return Response(status=status.HTTP_200_OK)
        else:
            print(otp1)
            return Response(otp1, status=status.HTTP_404_NOT_FOUND)


class UserOtpCode(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get('phone')
        otp = redis_code.get(phone)
        otp_code = serializer.validated_data.get('code')
        print(otp)
        if otp == otp_code:
            phone = '+98' + phone[1:]
            custom, created = User.objects.get_or_create(username=phone)
            refresh = RefreshToken.for_user(custom)
            access_token = refresh.access_token
            response_data = {
                'token': str(access_token),
                'refresh': str(refresh),
                'created': created
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "It`s wrong"}, status=status.HTTP_404_NOT_FOUND)


class Home(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response("ok", status=status.HTTP_200_OK)


class PostRetrivView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug_id):
        try:
            queryset = PostModel.objects.get(slug=slug_id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        response_data = {
            "id": queryset.id,
            "user": queryset.owner.username,
            "title": queryset.title,
            "slug": queryset.slug,
            "text": queryset.text,
            "created": queryset.created,
            "modified": queryset.modified,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializers()

    def post(self, request, *args, **kwargs):
        serializer = PostSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        text = serializer.validated_data['text']
        if PostModel.objects.filter(title=title).exists():
            return Response({"error": "title is already exist"}, status=status.HTTP_409_CONFLICT)
        queryset = PostModel.objects.create(text=text, title=title, owner=request.user)
        response_data = {
            "id": queryset.id,
            "user": queryset.owner.username,
            "title": queryset.title,
            "slug": queryset.slug,
            "text": queryset.text,
            "created": queryset.created,
            "modified": queryset.modified,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class PostUpdateView(APIView):
    permission_classes = [IsOwnerOrReadeOnly, IsAuthenticated]

    def put(self, request, slug_id):
        queryset = PostModel.objects.get(slug=slug_id)
        self.check_object_permissions(request, queryset)
        serializer = PostSerializers(instance=queryset, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if PostModel.objects.filter(title=serializer.validated_data['title']).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDeleteView(APIView):
    permission_classes = [IsOwnerOrReadeOnly, IsAuthenticated]

    def delete(self, request, slug_id):
        queryset = PostModel.objects.get(slug=slug_id)
        queryset.delete()
        return Response({'message': 'delete'}, status=status.HTTP_200_OK)
