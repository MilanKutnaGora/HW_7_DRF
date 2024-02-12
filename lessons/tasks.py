import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from lessons.models import CourseSubscription, Lesson
from users.models import User


@shared_task
def send_update_course(course_id):
    for sub in CourseSubscription.objects.filter(course_id=course_id):
        send_mail(
            subject='Обновление курса',
            message=f'Курс {sub.course} был обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sub.user.email]
        )


@shared_task
def send_add_lesson(lesson_id, course_id):
    for sub in CourseSubscription.objects.filter(course_id=course_id):
        send_mail(
            subject=f'Добавление урока {sub.course}',
            message=f'Урок {Lesson.objects.get(pk=lesson_id)} был добавлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[sub.user.email]
        )


@shared_task
def check_last_login():
    print("проверить последний вход пользователя ")
    now = datetime.datetime.now()
    now = timezone.make_aware(now, timezone.get_current_timezone())
    for user in User.objects.all():
        print(f"{user} - {user.last_login}")
        if user.last_login:
            print(now - user.last_login)
            if now - user.last_login > datetime.timedelta(days=31):
                user.is_active = False
                user.save()