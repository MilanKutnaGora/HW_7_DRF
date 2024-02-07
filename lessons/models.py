from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

PAY_CARD = 'card'
PAY_CASH = 'cash'

PAY_TYPES = (
    (PAY_CASH, 'наличные'),
    (PAY_CARD, 'перевод')
)

class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='lessons/', verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='название предмета')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='lessons/', verbose_name="картинка", **NULLABLE)
    link_video = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE,
                               related_name='lesson')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь',
                             on_delete=models.SET_NULL, **NULLABLE, related_name='payment')
    pay_date = models.DateField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_summ = models.IntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAY_TYPES, default=PAY_CASH, max_length=25, verbose_name='способ оплаты')
    is_successful = models.BooleanField(default=False, verbose_name='Статус платежа')
    session = models.CharField(max_length=150, verbose_name='cессия для оплаты', **NULLABLE)
    def __str__(self):
        return f'{self.user} - {self.pay_date}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'


class CourseSubscription(models.Model):
    is_subscribed = models.BooleanField(default=False, verbose_name='подписка', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', related_name='subscription')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.CASCADE,
                             related_name='course_user', **NULLABLE)

    def __str__(self):
        return f'Курс {self.course} - подписка {self.is_subscribed}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
