from django.urls import include, path
from rest_framework.routers import SimpleRouter

v1_router = SimpleRouter()

# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/
# v1_router.register('titles/(?P<titles_id>\\d+)/reviews', ReviewViewSet,
#                   basename='reviews')

# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
# http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
