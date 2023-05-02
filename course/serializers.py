from rest_framework import serializers
from django.contrib.auth.models import User

from course.models import *

__all__ = ['TeacherProfileSerializer', 'AdminProfileSerializer', 'StudentProfileSerializer',
           'GroupSerializer', 'LanguageSerializer', 'LessonSerializer', 'MarkSerializer',
           'StudentIdSerializer', 'StudentProfileRequestSerializer', 'AdminProfileRequestSerializer',
           'TeacherProfileRequestSerializer']


class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(source="user.username")
    first_name = serializers.EmailField(source="user.first_name")
    last_name = serializers.EmailField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = TeacherProfile
        fields = '__all__'


class AdminProfileSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(source="user.username")
    first_name = serializers.EmailField(source="user.first_name")
    last_name = serializers.EmailField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = AdminProfile
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(source="user.username")
    first_name = serializers.EmailField(source="user.first_name")
    last_name = serializers.EmailField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = StudentProfile
        fields = '__all__'


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


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'mark', 'description')


class StudentIdSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

