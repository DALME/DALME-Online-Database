from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView

from dalme_api.serializers.users import UserSerializer


class Auth(APIView):
    """API for JSON, refresh auth via ajax, supplemental to DalmeLogin."""
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def create_session(request, user):
        request.session.clear()
        request.session.cycle_key()
        request.session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        request.session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        request.session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
        request.session.save()

    def get(self, request):
        """403 stub for testing refresh auth flow."""
        return Response({'error': 'Not authenticated'}, 403)

    def post(self, request):
        """Login with JSON payload."""
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                serialized = UserSerializer(user, fields=['username', 'id'])
                response = Response(serialized.data, 200)
                self.create_session(request, user)
                response.set_cookie('sessionid', request.session.session_key)
                return response
        return Response({'error': 'Unauthorized'}, 401)
