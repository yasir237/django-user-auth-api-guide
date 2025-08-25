from datetime import date, datetime, timedelta
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils.crypto import get_random_string
from django.core.mail import send_mail


@api_view(["POST"])
def register(request):
    data = request.data
    user = SignUpSerializer(data=data)


    if not user.is_valid():
        return Response(user.errors)
    
    if User.objects.filter(username=data["email"]).exists():
        return Response({'details': 'This email already exists!'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create(
        username=data['email'],
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=make_password(data["password"]),
    )

    return Response({'details': 'Your account resgistered successfully!'}, status=status.HTTP_201_CREATED)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    data = request.data

    # Mevcut kullanıcı bilgilerini güncelle
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.email = data.get('email', user.email)
    user.username = data.get('email', user.username)  # username email olarak tutuluyor

    # Şifre güncelleme opsiyonel
    if data.get('password'):
        user.set_password(data['password'])

    user.save()

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
    


def get_current_hsot(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()

    return "{protocol}://{host}/".format(protocol=protocol, host=host)



@api_view(["POST"])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=20)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date

    user.profile.save()
    
    host = get_current_hsot(request)
    link = "{host}api/account/reset_password/{token}".format(host=host, token=token)

    body = (
        f"Hello {user.first_name},\n\nWe received a request to reset your password."
        f" Please use the link below to set a new password. This link will expire in 20 minutes.\n\nReset Password Link: {link}"
        "\n\nIf you did not request a password reset, please ignore this email."
    )

    send_mail(
        "Password Reset Request for Your Account",
        body,
        "no-reply@example.com",
        [user.email],
        fail_silently=False,
    )


    return Response({'details': f'A password reset link has been sent to {user.email}.'})



@api_view(["POST"])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, profile__reset_password_token=token)

    if user.profile.reset_password_expire < date.today():
        return Response({'error': 'The reset link has expired.'}, status=status.HTTP_400_BAD_REQUEST)

    if data['password'] != data['confirm_password']:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(data['password'])
    user.profile.reset_password_token = ''
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()

    return Response({'details': 'Your password has been reset successfully.'})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, id):
    if request.user.id == id:
        return Response({'error': 'You cannot delete your own account.'}, status=status.HTTP_400_BAD_REQUEST)

    user = get_object_or_404(User, id=id)
    user.delete()
    return Response({'details': 'Your account has been deleted.'})