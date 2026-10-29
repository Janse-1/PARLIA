from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Formatea todas las excepciones de DRF según la especificación de ARQUITECTURE.md (Sección 5.2).
    """
    response = exception_handler(exc, context)

    if response is not None:
        code = getattr(exc, 'default_code', 'API_ERROR').upper()
        detail = response.data.get('detail') if isinstance(response.data, dict) else None
        message = str(detail) if detail else 'Error al procesar la solicitud.'
        details = {} if detail else (response.data if isinstance(response.data, dict) else {'errors': response.data})

        response.data = {
            'status': 'error',
            'code': code,
            'message': message,
            'details': details,
        }

    return response

