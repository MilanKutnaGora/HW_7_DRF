from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from lessons.models import Course, Lesson, Payment, CourseSubscription
from lessons.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field="title", queryset=Course.objects.all())
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(url='link_video')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        if obj.lessons.all():
            return obj.lessons.all().count()
        return 0

    def get_subscription(self, obj):
        return CourseSubscription.objects.filter(course=obj,
                                                 user=self.context['request'].user).exists()
    class Meta:
        model = Course
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('paid_course', 'payment_type')

class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(fields=['course'],
                                                queryset=CourseSubscription.objects.all())
            ]




