from rest_framework import filters
from rest_framework.throttling import AnonRateThrottle
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Comment, Group, Post
from api.serializers import (
    CommentSerializer, GroupSerializer,
    PostSerializer, FollowSerializer
)
from api.permissions import IsAuthorOrReadOnlyPermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )
    throttle_classes = (AnonRateThrottle,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )
    throttle_classes = (AnonRateThrottle,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post=post_id)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (
        IsAuthorOrReadOnlyPermission,
    )
    throttle_classes = (AnonRateThrottle,)
    pagination_class = LimitOffsetPagination


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = (
        IsAuthenticated,
        IsAuthorOrReadOnlyPermission,
    )
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter
    )
    filterset_fields = ('following__username',)
    throttle_classes = (AnonRateThrottle,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
