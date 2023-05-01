from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, extend_schema_field, \
    extend_schema_serializer, OpenApiExample
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response

from course.models import *
from course.serializers import *


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='teacher_id',
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='language_id',
                type=OpenApiTypes.INT,
            ),
        ],
    )
)
class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        teach_id = self.request.query_params.get('teacher_id')
        lang_id = self.request.query_params.get('language_id')
        if teach_id is not None:
            return Group.objects.filter(teacher_id=teach_id)
        elif lang_id is not None:
            return Group.objects.filter(language_id=lang_id)
        return Group.objects.all()


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='group_id',
                type=OpenApiTypes.INT,
            ),
        ],
    )
)
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer

    def get_queryset(self):
        gr_id = self.request.query_params.get('group_id')
        if gr_id is not None:
            return Lesson.objects.filter(group_id=gr_id)
        return Lesson.objects.all()


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='student_id',
                type=OpenApiTypes.INT,
            ),
        ],
    )
)
class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer

    def get_queryset(self):
        stud_id = self.request.query_params.get('student_id')
        if stud_id is not None:
            return Mark.objects.filter(group_membership__student_id=stud_id)
        return Mark.objects.all()


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer


class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
