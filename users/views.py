from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
# from rest_framework import serializers

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from .models import Profile


class RegisterView(generics.CreateAPIView):
    # user = User.objects.get(pk=34)
    # posts = user.posts.all()
    # print(posts)

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile
    serializer_class = ProfileSerializer

    # def get(self, request):
    #     profile = Profile.objects.get(user=request.user)
    #     serializer = self.get_serializer(profile)
    #     return Response(serializer.data)
