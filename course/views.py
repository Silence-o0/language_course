from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, extend_schema_field, \
    extend_schema_serializer, OpenApiExample
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework import status

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
            OpenApiParameter(
                name='student_id',
                type=OpenApiTypes.INT,
            ),
        ],
    ),
    assign_student_to_group=extend_schema(
        request=StudentIdSerializer,
    ),
)
class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer

    def get_queryset(self):
        teach_id = self.request.query_params.get('teacher_id')
        lang_id = self.request.query_params.get('language_id')
        stud_id = self.request.query_params.get('student_id')
        if teach_id is not None:
            return Group.objects.filter(teacher_id=teach_id)
        elif lang_id is not None:
            return Group.objects.filter(language_id=lang_id)
        if stud_id is not None:
            return Group.objects.filter(studentprofile__id=stud_id)
        return Group.objects.all()

    @action(detail=True, methods=['post'])
    def assign_student_to_group(self, request, *args, **kwargs):
        group = self.get_object()
        serializer_class = StudentIdSerializer(data=request.data)
        if serializer_class.is_valid():
            try:
                student = StudentProfile.objects.get(id=serializer_class.validated_data['id'])
            except StudentProfile.DoesNotExist:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
            group.studentprofile_set.add(student)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path=r'remove_student_from_group/(?P<student_id>\w+)')
    def remove_student_from_group(self, request,  *args, **kwargs):
        group = self.get_object()
        student_id = kwargs.get('student_id')

        if student_id is not None and group is not None:
            student = StudentProfile.objects.get(id=student_id)
            group.studentprofile_set.remove(student)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer

    def get_queryset(self):
        gr_id = self.request.query_params.get('group_id')
        if gr_id is not None:
            return StudentProfile.objects.filter(groups__id=gr_id)
        return StudentProfile.objects.all()
