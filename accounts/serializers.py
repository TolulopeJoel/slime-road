from rest_framework import serializers

from django.contrib.auth import get_user_model


class CreatorSerializer(serializers.ModelSerializer):
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
