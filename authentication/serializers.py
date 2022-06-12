from rest_framework import serializers
from django.contrib. auth import get_user_model,authenticate
from django.contrib.auth.models import Permission
from .models import User
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    first_name = serializers.CharField(
        write_only=True
    )
    last_name = serializers.CharField(
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name','last_name', 'password','token']

    def create(self, validated_data):
        return User.objects.create_superuser(email=validated_data["email"],password=validated_data["password"],first_name=validated_data["first_name"],last_name=validated_data["last_name"])


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.SerializerMethodField()
    def get_role(self,obj):
        return 'ADMIN'
    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'token': str(user.token),
            'role': 'admin'
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'