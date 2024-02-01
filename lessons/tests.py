from django.test import TestCase

from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

from lessons.models import Lesson, Course, CourseSubscription
from users.models import User


class LessonsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )

    def test_lesson_create(self):
        data = {
            'title': 'Test lesson',
            'description': 'Test description',
            'course': 'self.course',
            'link_video': 'https://www.youtube.com/watch?v=rCLDTrFNP4E'
        }
        response = self.client.post(
            reverse('lessons:lesson-create'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.count(),
            2
        )

    def test_lesson_list(self):
        response = self.client.get(
            reverse('lessons:lesson-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'count': 1, 'next': None, 'previous': None, 'results': [
                {'id': self.lesson.id, 'course': 'Test course', 'title': 'Test lesson',
                 'description': 'Test description',
                 'preview': None, 'link_video': None, 'owner': self.lesson.owner.id}]}

        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse('lessons:lesson-get',
                    args=[self.lesson.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'course': 'Test course', 'title': 'Test lesson', 'description': 'Test description',
             'preview': None, 'link_video': None, 'owner': self.lesson.owner.id}
        )

    def test_lesson_update(self):
        data = {
            'title': 'Test update title',
            'description': 'Test update description',
            'course': self.course,
            'link_video': 'https://www.youtube.com/watch?v=rCLDTrFNP4E'
        }
        response = self.client.put(
            reverse('lessons:lesson-update', args=[self.lesson.id]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {'id': self.lesson.id, 'course': 'Test course', 'title': 'Test update title',
             'description': 'Test update description',
             'preview': None,
             'link_video': 'https://www.youtube.com/watch?v=rCLDTrFNP4E',
             'owner': self.lesson.owner.id}
        )

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse('lessons:lesson-delete', args=[self.lesson.id])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.count(),
            0
        )

    def tearDown(self):
        pass


class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@sky.pro', is_active=True)
        self.user.set_password('test_password')
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Test course')
        self.lesson = Lesson.objects.create(
            title='Test lesson',
            description='Test description',
            course=self.course,
            owner=self.user,
        )
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription_create(self):
        course = Course.objects.create(title='Test course 2')
        course.save()

        data = {
            'course': course.id,
            'user': self.user.id
        }
        response = self.client.post(
            reverse('lessons:subs-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            2
        )

    def test_subscription_list(self):
        response = self.client.get(
            reverse('lessons:subs-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [{'id': self.subscription.id, 'is_subscribed': False, 'course': self.subscription.course.id,
              'user': self.subscription.user.id}]
        )

    def test_subscription_delete(self):
        response = self.client.delete(
            reverse('lessons:subs-delete', args=[self.subscription.id])
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            CourseSubscription.objects.count(),
            0
        )
