from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from djoser.serializers import UserCreateSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'password', 'date_joined']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'is_active', 'is_superuser', 'last_login', 'date_joined']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token if needed
        # token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Use CustomUserSerializer to serialize user details
        user_serializer = CustomUserSerializer(self.user)

        # Add custom user details to the response
        data['user_details'] = user_serializer.data

        # Add any other user details you want to include

        return data