from django.urls import path, include
from rest_framework_nested import routers
from .views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('posts', PostViewSet)

# Nested router for comments under posts
posts_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')
posts_router.register('comments', CommentViewSet, basename='post-comments')

urlpatterns = router.urls  + posts_router.urls