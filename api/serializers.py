from rest_framework import serializers

from .models import EmailVerificationCode 


class EmailVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('id', 'email')