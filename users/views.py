from rest_framework.views import APIView
from rest_framework.response import Response

from background.settings import SECRET_KEY
from users.serializers import UserSerializer
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from background.settings import JWT_SECRET_KEY


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User was not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Wrong password for user')

        payload = {
            'id': user.id,
            "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
            "jwt": token
        }

        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Not authenticated!")

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Not authenticated!")

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("jwt")
        response.data = {
            "message": "Successfully logged out!"
        }

        return response

class AuthenticatedAPIView(APIView):
    def get_user_from_token(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Not authenticated!")

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Not authenticated!")

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        return user

class AdminAuthenticatedAPIView(AuthenticatedAPIView):
    def get_user_from_token(self, request):
        user = super().get_user_from_token(request)
        if not user.is_superuser:
            raise AuthenticationFailed("Admin access required!")
        return user