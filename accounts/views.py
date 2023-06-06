from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import login as auth_login
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts import serializers as account_serializers

User = get_user_model()


class UserSignUpAPIView(generics.CreateAPIView):
    serializer_class = account_serializers.UserSignUpSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(generics.GenericAPIView):
    serializer_class = account_serializers.UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request=request, username=username,
                            password=password)
        if user is not None:
            auth_login(request, user)
            return Response({'detail': 'Logged in successfully.'})
        else:
            return Response({'detail': 'Invalid credentials.'},
                            status=status.HTTP_401_UNAUTHORIZED)
