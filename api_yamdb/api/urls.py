from django.urls import include, path

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
