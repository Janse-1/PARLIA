from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class LoginAPIView(APIView):
    """
    POST /api/v1/auth/login/
    Autentica credenciales por correo institucional y devuelve token + perfil de estudiante.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'code': 'AUTHENTICATION_FAILED',
                    'message': 'Credenciales inválidas o datos incompletos.',
                    'details': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data['user']
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'status': 'success',
                'data': {
                    'token': token.key,
                    'user': UserSerializer(user).data,
                },
            },
            status=status.HTTP_200_OK,
        )


class RegisterAPIView(APIView):
    """
    POST /api/v1/auth/register/
    Registra un nuevo estudiante, inicia su sesión y devuelve token + perfil.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = 'No fue posible completar el registro. Verifica los datos ingresados.'
            for field_errors in serializer.errors.values():
                if isinstance(field_errors, list) and field_errors:
                    first_error = str(field_errors[0])
                    break
            return Response(
                {
                    'status': 'error',
                    'code': 'REGISTRATION_FAILED',
                    'message': first_error,
                    'details': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.save()
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'status': 'success',
                'data': {
                    'token': token.key,
                    'user': UserSerializer(user).data,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LogoutAPIView(APIView):
    """
    POST /api/v1/auth/logout/
    Revoca el token activo y cierra la sesión del usuario.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        logout(request)
        return Response(
            {
                'status': 'success',
                'data': {
                    'message': 'Sesión cerrada exitosamente.',
                },
            },
            status=status.HTTP_200_OK,
        )


class MeAPIView(APIView):
    """
    GET /api/v1/me/
    Devuelve la información del perfil del estudiante autenticado (extraído de request.user).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            {
                'status': 'success',
                'data': serializer.data,
            },
            status=status.HTTP_200_OK,
        )
