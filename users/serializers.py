from django.contrib.auth.models import User  # User 모델
from django.contrib.auth.password_validation import validate_password  # Django의 기본 패스워드 검증 도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Token 모델
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지를 위한 검증 도구

# Django의 기본 authenticate 함수, 설정한 DefaultAuthBackend 인 TokenAuth 방식으로 유저인증
from django.contrib.auth import authenticate
from .models import Profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    # write_only 옵션을 통해 client>server 방향의 역직렬화는 가능, server>client 방향의 직렬화는 불가능
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )


# 회원가입 시리얼라이즈
class RegisterSerializer(serializers.ModelSerializer):
    # 이메일 중복검증
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    # 비밀번호 검증
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    # 비밀번호 확인을 위한 필드
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data):
        # CREATE 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("nickname", "position", "subjects", "image")
