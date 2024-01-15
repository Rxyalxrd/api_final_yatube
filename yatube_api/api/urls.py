from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

first_router = DefaultRouter()

first_router.register('posts', PostViewSet, basename='posts')
first_router.register('groups', GroupViewSet, basename='groups')
first_router.register('follow', FollowViewSet, basename='follow')
first_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(first_router.urls)),
    path('v1/auth/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
