from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    program_display = serializers.CharField(source='get_program_display', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'program',
            'program_display',
            'date_joined',
        )
        read_only_fields = ('id', 'email', 'date_joined')

    def get_full_name(self, obj: User) -> str:
        name = f"{obj.first_name} {obj.last_name}".strip()
        return name if name else obj.username


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password,
            )
            if not user:
                raise serializers.ValidationError(
                    'Credenciales inválidas. Verifique su correo institucional y contraseña.',
                    code='INVALID_CREDENTIALS',
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    'Esta cuenta de estudiante se encuentra deshabilitada.',
                    code='ACCOUNT_DISABLED',
                )
        else:
            raise serializers.ValidationError(
                'Debe proporcionar correo electrónico y contraseña.',
                code='MISSING_CREDENTIALS',
            )

        attrs['user'] = user
        return attrs

