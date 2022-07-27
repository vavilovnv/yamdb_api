from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator

from .serializers import CreateTokenSerializer, SignUpSerializer


def send_email(user, code):
    email = EmailMessage(
        subject='Код верификации для доступа к API yamdb',
        body=code,
        to=(user.email,)
    )
    email.send()


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # user = serializer.save()
    # send_email(
    #     user,
    #     default_token_generator.make_token(user)
    # )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_token(request):
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.data['username']
    is_token_ok = default_token_generator.check_token(
        user,
        serializer.data['confirmation_code']
    )
    if is_token_ok:
        return Response(
            {'token': str(RefreshToken.for_user(user).access_token)},
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
