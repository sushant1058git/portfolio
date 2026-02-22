from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return Response({
                    'success': True,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                    }
                })
            else:
                return Response(
                    {'error': 'Access denied. Staff privileges required.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'success': True})


class AuthCheckView(APIView):
    def get(self, request):
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            return Response({
                'authenticated': True,
                'user': {
                    'username': request.user.username,
                    'email': request.user.email,
                    'is_staff': request.user.is_staff,
                }
            })
        return Response({'authenticated': False})
