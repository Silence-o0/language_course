from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

from course.models import *

__all__ = ['TeacherProfileSerializer', 'AdminProfileSerializer', 'StudentProfileSerializer',
           'GroupSerializer', 'LanguageSerializer', 'LessonSerializer', 'MarkSerializer',
           'StudentIdSerializer', 'StudentProfileRequestSerializer', 'AdminProfileRequestSerializer',
           'TeacherProfileRequestSerializer', 'StudentProfileListSerializer', 'TeacherProfileListSerializer',
           'MarkRequestSerializer', 'MarkUpdateSerializer']


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = TeacherProfile
        fields = '__all__'


class AdminProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = AdminProfile
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'


class StudentProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = StudentProfile
        fields = ('user_id', 'username', 'first_name', 'last_name')
        read_only_fields = ('user_id',)


class TeacherProfileListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = TeacherProfile
        fields = ('username', 'first_name', 'last_name')


class StudentProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'


class AdminProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = '__all__'


class TeacherProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

    def validate(self, data):
        if data['time_start'] >= data['time_finish']:
            raise serializers.ValidationError("finish must occur after start")
        gr_id = data['group'].id
        teach_id = TeacherProfile.objects.get(group__id=gr_id)
        queryset = Lesson.objects.filter(group__teacher_id=teach_id)
        queryset = queryset.filter(day_week=data['day_week'])
        for lesson in queryset:
            if (lesson.time_start < data['time_start'] < lesson.time_finish) or \
                    (lesson.time_start < data['time_finish'] < lesson.time_finish):
                raise serializers.ValidationError("This teacher already has a lesson on this time")
        return data


class MarkSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source="group_membership.student_id")
    group_id = serializers.IntegerField(source="group_membership.group_id")

    class Meta:
        model = Mark
        fields = ('id', 'mark', 'description', 'student_id', 'group_id')


class MarkRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('mark', 'description', 'group_membership')


class MarkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('mark', 'description')


class StudentIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = ('id',)


class UserRegisterSerializer(UserCreateSerializer):
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)
    email = serializers.EmailField(allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate(self, data):
        queryset = User.objects.filter(email=data['email'])
        if queryset is None:
            return data
        else:
            raise serializers.ValidationError({'email': ["User with such email is already exist.", ]})


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'id')
        read_only_fields = ('username', 'email', 'id')
