from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from users.models import Profile
from .models import Post
from .permissions import CustomReadOnly
from .serializers import PostSerializer, PostCreateSerializer

import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger('my')

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [CustomReadOnly]

    def get_serializer_class(self):
        logger.info(self.action)
        if self.action == ('list' or 'retrieve'):
            return PostSerializer
        return PostCreateSerializer

    def perform_create(self, serializer):
        logger.info("perform_create")
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=self.request.user, profile=profile)

