from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, action

from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Comment, Review

from .permissions import AdminPermission
from .serializers import (CommentSerializer, ReviewSerializer, UserSerializer,
                          UserSerializerReadOnly)

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """API для работы пользователями."""


    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        """Запрос информации пользователя о себе, редактирование профиля
         пользователя."""

        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializerReadOnly(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


def send_email(username, email, code):
    """Отправка письма с кодом подтверждения на почту регистрируемому
    пользователю."""

    send_mail(
        'Подтверждение регистрации на сайте yamdb.',
        (f'Для получения токена и подтверждения регистрации сделайте '
         f'post-запрос со следующими параметрами:\n'
         f'username : {username}\n'
         f'confirmation_code: {code}'),
        'noreply@api_yamdb.com',
        [email],
        fail_silently=False,
    )


def response_400(fields, data):
    """Возврат списка названий неправильных полей переданных в запросы."""

    return Response(
        {'field_name': list(filter(
            lambda f: f not in data,
            [field for field in fields]
        ))},
        status=status.HTTP_400_BAD_REQUEST
    )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


@api_view(['POST'])
def signup_user(request):
    """Регистрация кода подтверждения для пользователя."""

    fields = ('username', 'email')
    if not all([f in request.data for f in fields]):
        return response_400(fields, request.data)
    username = request.data.get('username')
    email = request.data.get('email')
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    send_email(username, email, confirmation_code)
    return Response({'email': email}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_token(request):
    """Проверка кода подтверждения и возврат токена пользователю."""

    fields = ('username', 'confirmation_code')
    if not all([f in request.data for f in fields]):
        return response_400(request.data)
    username = request.data.get('username')
    confirmation_code = request.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    is_token_ok = default_token_generator.check_token(
        user=user,
        token=confirmation_code
    )
    if is_token_ok:
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
