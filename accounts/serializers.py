from rest_framework import serializers
from django.contrib.auth import get_user_model


class CreatorSerializer(serializers.ModelSerializer):
    """
    Serializer for the creator (user) model.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'bio',
            'profile_picture',
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'username',
            'password',
            'password2'
        ]

    def create(self, validated_data):
        """
        Create a new user based on the validated data.
        """
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(**validated_data)
        return user

    def validate(self, attrs):
        """
        Validate the user data before creating a new user.
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError('Passwords must match')
        return attrs
