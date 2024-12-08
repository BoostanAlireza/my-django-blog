from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet)
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('profiles', views.ProfileViewSet)

posts_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
posts_router.register('comments', views.CommentViewSet, basename='post-comments')
posts_router.register('images', views.PostImageViewSet, basename='post-images')

# categories_router = routers.NestedDefaultRouter(router, 'categories', lookup='category')
# categories_router.register('posts', views.CategoryPostViewSet, basename='category-posts')

urlpatterns = router.urls + posts_router.urls 