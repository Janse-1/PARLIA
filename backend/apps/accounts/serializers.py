from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import AcademicProgram, User


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


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    program = serializers.ChoiceField(
        choices=AcademicProgram.choices,
        default=AcademicProgram.SISTEMAS,
    )
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_email(self, value: str) -> str:
        normalized = value.strip().lower()
        if User.objects.filter(email__iexact=normalized).exists():
            raise serializers.ValidationError(
                'Ya existe una cuenta registrada con este correo electrónico.'
            )
        return normalized

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password_confirm and password != password_confirm:
            raise serializers.ValidationError(
                {'password_confirm': 'Las contraseñas no coinciden.'}
            )

        temp_user = User(
            email=attrs.get('email', ''),
            username=attrs.get('email', ''),
            first_name=attrs.get('first_name', '').strip(),
            last_name=attrs.get('last_name', '').strip(),
            program=attrs.get('program', AcademicProgram.SISTEMAS),
        )
        try:
            validate_password(password, user=temp_user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})

        return attrs

    def create(self, validated_data):
        email = validated_data['email']
        base_username = email.split('@')[0][:120] or 'estudiante'
        username = base_username
        counter = 1
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            first_name=validated_data['first_name'].strip(),
            last_name=validated_data['last_name'].strip(),
            program=validated_data.get('program', AcademicProgram.SISTEMAS),
        )
        return user
