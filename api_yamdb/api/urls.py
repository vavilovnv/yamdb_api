from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UsersViewSet
from .views import signup, create_token

router_v1 = DefaultRouter()
router_v1.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', create_token, name='token'),
    path('v1/', include(router_v1.urls)),
]