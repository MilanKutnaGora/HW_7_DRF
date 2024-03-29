from django.urls import path
from rest_framework import routers

from lessons.apps import LessonsConfig
from lessons.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, PaymentCreateAPIView, PaymentRetrieveAPIView

app_name = LessonsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson-delete'),

    #payment
    path('payment/', PaymentListAPIView.as_view(), name='payment-list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment-create'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment-detail'),

    # subscription
    path('subscriptions/', SubscriptionListAPIView.as_view(), name='subs-list'),
    path('subscriptions/create/', SubscriptionCreateAPIView.as_view(), name='subs-create'),
    path('subscriptions/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subs-delete'),

] + router.urls