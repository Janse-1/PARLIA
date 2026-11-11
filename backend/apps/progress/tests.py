from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import AcademicProgram, User
from apps.learning.models import Lesson, Module
from apps.progress.models import LearningProgress, ProgressStatus


class ProgressAntiIDORSecurityTests(APITestCase):
    def setUp(self):
        self.student_a = User.objects.create_user(
            username='estudiante_a',
            email='estudiante_a@uniguajira.edu.co',
            password='ParliaPasswordA2026*',
            first_name='Andres',
            last_name='Ipuana',
            program=AcademicProgram.SISTEMAS,
        )
        self.student_b = User.objects.create_user(
            username='estudiante_b',
            email='estudiante_b@uniguajira.edu.co',
            password='ParliaPasswordB2026*',
            first_name='Maria',
            last_name='Jusayu',
            program=AcademicProgram.INDUSTRIAL,
        )
        self.module = Module.objects.create(
            title='Módulo de Prueba Anti-IDOR',
            slug='modulo-prueba-anti-idor',
            description='Descripción de prueba',
            order=99,
            is_published=True,
        )
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='Lección 1 Anti-IDOR',
            slug='leccion-1-anti-idor',
            content='Contenido',
            order=1,
            is_published=True,
        )

    def test_student_cannot_modify_another_student_progress_via_idor_payload(self):
        """
        Verifica que aunque un usuario autenticado (student_a) envíe `user` o `user_id`
        apuntando a `student_b` en POST /api/v1/progress/, el registro sólo afecta a `student_a`.
        """
        self.client.force_authenticate(user=self.student_a)
        upsert_url = reverse('progress-upsert')

        malicious_payload = {
            'user': self.student_b.id,
            'user_id': self.student_b.id,
            'lesson_id': self.lesson.id,
            'status': ProgressStatus.COMPLETED,
        }
        response = self.client.post(upsert_url, malicious_payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED))

        # El progreso de student_b debe permanecer intacto (sin registros)
        self.assertFalse(
            LearningProgress.objects.filter(user=self.student_b, lesson=self.lesson).exists()
        )
        # El registro se creó únicamente para student_a (request.user)
        self.assertTrue(
            LearningProgress.objects.filter(
                user=self.student_a,
                lesson=self.lesson,
                status=ProgressStatus.COMPLETED,
            ).exists()
        )

    def test_my_progress_returns_only_authenticated_user_records(self):
        LearningProgress.objects.create(
            user=self.student_b,
            lesson=self.lesson,
            status=ProgressStatus.COMPLETED,
        )

        self.client.force_authenticate(user=self.student_a)
        me_progress_url = reverse('progress-me')
        response = self.client.get(me_progress_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']['records']), 0)
