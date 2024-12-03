from django.contrib.auth.models import User
from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer


class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True, required=True)
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            'id', 'username', 'password', 're_password', 'email', 'first_name', 'last_name'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return super().validate(attrs)
      
    def create(self, validated_data):
        validated_data.pop('repeat_password', None)
        return super().create(validated_data)

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']