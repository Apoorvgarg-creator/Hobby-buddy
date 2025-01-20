from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )

        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, validated_data):
        username = validated_data['username']
        password=validated_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                validated_data['user'] = user
                return validated_data 
            raise serializers.ValidationError("Invalid username or password")
        raise serializers.ValidationError("Invalid username or password")
    