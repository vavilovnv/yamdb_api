from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django_filters.rest_framework import DjangoFilterBackend

from django.core.mail import send_mail

from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, filters, generics
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Comment, Review, Category, Genre, Title

from .permissions import AdminPermission, AdminOrReadOnly
from .serializers import (CommentSerializer, ReviewSerializer,
                          CategorySerializer, GenreSerializer,
                          ReadTitleSerializer, CreateTitleSerializer,
                          UserSerializer, UserSerializerReadOnly,
                          SignupSerializer, CreateTokenSerializer)

User = get_user_model()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CategoryList(generics.ListCreateAPIView):
    """Получение списка/Создание категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """Изменение/удаление категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)


class GenreList(generics.ListCreateAPIView):
    """Получение списка/Создание жанра"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    """Изменение/удаление жанра"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = ReadTitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ['category__slug', 'genre__slug', 'name', 'year']
    search_fields = ['category__slug', 'genre__slug']

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTitleSerializer
        return super().get_serializer_class()


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
         f'username: {username}\n'
         f'confirmation_code: {code}'),
        'noreply@api_yamdb.com',
        [email],
        fail_silently=False,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    """Регистрация кода подтверждения для пользователя."""

    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, created = User.objects.get_or_create(
        username=username,
        email=email,
    )
    confirmation_code = default_token_generator.make_token(user)
    send_email(username, email, confirmation_code)
    return Response(
        {'email': email, 'username': username},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def create_token(request):
    """Проверка кода подтверждения и возврат токена пользователю."""

    serializer = CreateTokenSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(status=status.HTTP_404_NOT_FOUND)
    username = serializer.data['username']
    confirmation_code = serializer.data['confirmation_code']
    user = get_object_or_404(User, username=username)
    is_token_ok = default_token_generator.check_token(
        user=user,
        token=confirmation_code
    )
    if is_token_ok:
        token = RefreshToken.for_user(user).access_token
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
