
import random
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .models import EmailVerificationCode, Title
from rest_framework.decorators import api_view, permission_classes
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser
from rest_framework.pagination import PageNumberPagination
from .serializers import CodeVerificationSerializer, EmailVerificationCodeSerializer, TitleSerializer, UserSerializer
from rest_framework import permissions
from rest_framework import generics
from rest_framework.views import APIView

# Надо самостоятельно описать необходимые методы.
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
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
@permission_classes([permissions.AllowAny])
def check_verification_code(request):
    """
    Получает код подтверждения, проверяет его на валидность.
    По полученному email определяем пользователя.
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
        return Response({"detail": "Пользователя с таким email нет."},status=400)
    if not obj.is_expired() and confirmation_code == obj.confirmation_code:

        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token)})
    return Response({"detail": "Неправильный код"}, status=402)

class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    permission_classes = (permissions.IsAdminUser,)

    
    def get_serializer_class(self):
        return super().get_serializer_class()\

class UserGetPatchView(APIView):
    def get(self,request):
        user_profile = get_object_or_404(CustomUser, username=request.user)
        serializer = UserSerializer(user_profile)
        return Response(serializer.data, status=200)
    
    def patch(self, request):
        user = get_object_or_404(CustomUser, username = request.user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data["role"] == "admin":
            user.is_staff = True
        serializer.save()
        return Response(serializer.data, status=201)
    
class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.AllowAny,)
    # def get_permissions(self):
    #     # Если в GET-запросе требуется получить информацию об объекте
    #     if self.action == 'retrieve' or self.action == 'list':
    #         # Вернём обновлённый перечень используемых пермишенов
    #         return (permissions.AllowAny,)
    #     # Для остальных ситуаций оставим текущий перечень пермишенов без изменений
    #     return (permissions.IsAdminUser,)
