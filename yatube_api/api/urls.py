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
    path('', include(first_router.urls)),
    path('auth/', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
