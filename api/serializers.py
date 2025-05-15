from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailVerificationCode 
from users.models import CustomUser


class EmailVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('id', 'email')


class CodeVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=6, required=True)
    class Meta:
        model = EmailVerificationCode
        fields = ('id', 'email', "confirmation_code")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'