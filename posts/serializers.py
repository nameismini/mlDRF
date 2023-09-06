# posts/serializers.py
from rest_framework import serializers

from users.serializers import ProfileSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)  # nested serializer

    class Meta:
        model = Post
        fields = {"pk", "profile", "title", "category", "body", "image", "likes", "published_date"}


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = {"title", "category", "body", "image"}
