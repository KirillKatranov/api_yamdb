
import random

from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationCode
from rest_framework.decorators import api_view
from django.core.mail import send_mail

from .serializers import EmailVerificationCodeSerializer

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
    EmailVerificationCode.objects.create(email=email, code=code)
    # Отправка письма
    send_mail(
        subject="Ваш код подтверждения",
        message=f"Ваш код подтверждения: {code}",
        from_email="katranov2@yandex.ru",
        recipient_list=[email],
    )
    return Response({"detail": "Код отправлен на email"}, status=200)





