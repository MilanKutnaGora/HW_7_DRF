from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, serializers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from lessons.models import Course, Lesson, Payment, CourseSubscription
from lessons.paginators import CoursePaginator, LessonPaginator
from lessons.permissions import IsModerator, IsOwnerOrStaffUser
from lessons.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscribeSerializer, \
    PaymentCreateSerializer
from lessons.services import get_session, retrieve_session
from lessons.tasks import send_add_lesson, send_update_course


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course_id = serializer.save(owner=self.request.user).id
        send_update_course.delay(course_id)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        course_id = serializer.save(owner=self.request.user).course.id
        lesson_id = serializer.save(owner=self.request.user).id
        send_add_lesson.delay(course_id, lesson_id)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = LessonPaginator

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaffUser]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrStaffUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_type',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentCreateSerializer



    def perform_create(self, serializer):
        course = serializer.validated_data.get('paid_course')
        if not course:
            raise serializers.ValidationError('Не указан курс.')
        payment = serializer.save()
        payment.user = self.request.user
        if payment.payment_type == 'card':
            payment.session = get_session(payment).id
        payment.save()


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if obj.session:
            session = retrieve_session(obj.session)
            if session.payment_status == 'paid' and session.status == 'complete':
                obj.is_successful = True
                obj.save()
        self.check_object_permissions(self.request, obj)
        return obj



class SubscriptionCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, IsModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return CourseSubscription.objects.filter(user=self.request.user)


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = CourseSubscription.objects.all()
    permission_classes = [IsAuthenticated, IsModerator]
