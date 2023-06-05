from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from django.conf import settings
from django.contrib.auth import login, logout

from .models import AccessToken, User

from .serialrizers import LoginSerializer, RegisterSerializer, UserSerializer,ConfirmSerializer



class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(UserID=serializer.validated_data["UserID"])
            userid = serializer.validated_data['UserID']
            token = AccessToken.create(user)
            return Response({'detail': "ログインが成功しました。", 'error': 0, 'token': token.token, 'UserID': userid})
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)


# 新規登録処理
# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # すでにEmailが使われている場合
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)

            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # UserIDがすでに使われていた場合
            if User.objects.filter(UserID=serializer.validated_data['UserID']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                serializer.save()
            except:
                # データベースエラー
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # すでにEmailが使われている場合
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)

            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # UserIDがすでに使われていた場合
            if User.objects.filter(UserID=serializer.validated_data['UserID']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            serializer.save()
            # エラーなし
            try:
                serializer.save()
            except:
                # データベースエラー
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# アカウント承認処理
class ConfirmView(APIView):
    @staticmethod
    def post(request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            # マッチした場合
            user = User.objects.filter(UserID=serializer.validated_data['UserID'],
                                       token=serializer.validated_data['token'])
            # すでにEmailが使われている場合
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)
            # パスワードと確認パスワードが一致しない場合
            if serializer.validated_data['password'] != request.data['password_confirmation']:
                return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # UserIDがすでに使われていた場合
            if User.objects.filter(UserID=serializer.validated_data['UserID']).exists():
                return Response({'error': 3}, status=HTTP_400_BAD_REQUEST)

            # Enable user account
            try:
                user.update(enabled=True)
            except:
                return Response({'error': 11}, status=HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


# ユーザー情報取得処理
class DataView(APIView):
    @staticmethod
    def post(request):
        user = User.objects.filter(access_token=request.data['access_token'], UserID=request.data['UserID'])
        if not user.exists():
            return Response(status=HTTP_404_NOT_FOUND)
        user.first()
        return Response(serializer.data, status=HTTP_200_OK)


# ログアウト
class LogoutView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        logout(request)
        return Response({'detail': "ログアウトが成功しました。"})
    
