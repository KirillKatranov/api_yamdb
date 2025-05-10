
import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationCode
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser

from .serializers import CodeVerificationSerializer, EmailVerificationCodeSerializer

# Надо самостоятельно описать необходимые методы.
@api_view(['POST'])
def send_verification_code(request):
    """
    Получает email, проверяет его валидность,
    генерирует код, отправляет код на этот email. 
    """
    serializer = EmailVerificationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"] 
    
    code = f"{random.randint(100000, 999999)}"
    EmailVerificationCode.objects.create(email=email,     confirmation_code=code)
    # Отправка письма
    send_mail(
        subject="Ваш код подтверждения",
        message=f"Ваш код подтверждения: {code}",
        from_email="katranov2@yandex.ru",
        recipient_list=[email],
    )
    return Response({"detail": "Код отправлен на email"}, status=200)

@api_view(['POST'])
def check_verification_code(request):
    """
    Получает код подтверждения, проверяет его на валидность.
    В случае успеха возвращает ответ с токеном, иначе ошибка 400 
    и возможно кастомный ответ.
    """
    serializer = CodeVerificationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    obj = EmailVerificationCode.objects.filter(email=email).order_by('-created_at').first()
    user = get_object_or_404(CustomUser, email=email)
    if obj is None:
        return Response(status=400)
    if not obj.is_expired() and confirmation_code == obj.confirmation_code:

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token)})
    return Response(status=402)
    
