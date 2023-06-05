from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserFollow


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        exclude = ('created_at', 'deleted_at')


# ログイン処理
class LoginSerializer(serializers.Serializer):
    UserID = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        UserID = data.get('UserID')
        password = data.get('password')
        userid = User.objects.get(UserID=UserID)
        re_password = User.objects.get(password=password)
        print(UserID)
        print(password)
        print(userid.UserID)
        print(re_password.password)
        if UserID == userid.UserID:
            if password == re_password.password:
                return data

            else:
                raise serializers.ValidationError('ログイン失敗')


# ここのUserSerialzerは全てのフィールドを表すシリアルライザー
# このシリアルライザーを使用するとUserモデルの全てのフィールドを表示
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['UserID', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}


# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
# これは新規登録用のシリアルライザー、新規登録に必要なフィールドだけを記述
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('UserID','name','email','password')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user


# ユーザー承認に必要なデータを受け取るシリアルライザーを作成
class ConfirmSerializer(serializers.Serializer):
    UserID = serializers.CharField()
    token = serializers.CharField()
    error = serializers.IntegerField(required=False)


# フォローシリアルライザ
class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ["user", "follow"]

        def create(self, validated_data):
            user = UserFollow.objects.create_user(**validated_data)
            return user


# フォロワーシリアルライザ
class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ("user")