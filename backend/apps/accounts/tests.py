from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import AcademicProgram, User


class AuthAndRegistrationTests(APITestCase):
    def test_self_service_student_registration_and_login(self):
        register_url = reverse('auth-register')
        payload = {
            'first_name': 'Laura',
            'last_name': 'Pushaina',
            'email': 'laura.pushaina@uniguajira.edu.co',
            'program': AcademicProgram.SISTEMAS,
            'password': 'ParliaSecurePassword2026!',
            'password_confirm': 'ParliaSecurePassword2026!',
        }
        response = self.client.post(register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('token', response.data['data'])
        self.assertEqual(
            response.data['data']['user']['email'],
            'laura.pushaina@uniguajira.edu.co',
        )
        self.assertNotIn('password', response.data['data']['user'])
