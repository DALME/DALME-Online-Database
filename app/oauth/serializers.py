"""Define serializers for the oauth application."""

from rest_framework import serializers

from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """Serializer for session login."""

    username = serializers.CharField(label='username', write_only=True)
    password = serializers.CharField(
        label='password', style={'input_type': 'password'}, trim_whitespace=True, write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Access denied: incorrect username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required fields.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
