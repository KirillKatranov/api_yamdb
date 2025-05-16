from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, EmailVerificationCode, Genre, Title 
from users.models import CustomUser


class EmailVerificationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('id', 'email')


class CodeVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailVerificationCode
        fields = ('id', 'email', "confirmation_code")

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'role']


class TitleSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    year = serializers.CharField(required=False)
    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']

class GenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Genre
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]