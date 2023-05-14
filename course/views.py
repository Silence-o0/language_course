from django.core.mail import send_mail
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view, extend_schema_field, \
    extend_schema_serializer, OpenApiExample
from rest_framework import viewsets, filters, mixins
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from course.models import *
from course.policy import *
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
    permission_classes = (GroupAccessPolicy,)

    def get_queryset(self):
        user = self.request.user
        query_params = self.request.query_params
        queryset = Group.objects.all()
        if user.groups.filter(name="student").exists():
            queryset = queryset.filter(groupmembership__student__user=user)
        if user.groups.filter(name="teacher").exists():
            queryset = queryset.filter(teacher_id=user.id)
        if teach_id := query_params.get('teacher_id'):
            if user.groups.filter(name="teacher").exists():
                if int(user.teacherprofile.user_id) != int(teach_id):
                    return None
            queryset = queryset.filter(teacher_id=teach_id)
        if lang_id := query_params.get('language_id'):
            queryset = queryset.filter(language_id=lang_id)
        if stud_id := query_params.get('student_id'):
            if user.groups.filter(name="student").exists():
                if int(user.studentprofile.user_id) != int(stud_id):
                    return None
            queryset = queryset.filter(studentprofile__user_id=stud_id)
        return queryset

    @action(detail=True, methods=['post'])
    def assign_student_to_group(self, request, *args, **kwargs):
        user = self.request.user
        group = self.get_object()
        if not user.groups.filter(name="teacher").exists() and not user.groups.filter(name="admin").exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif user.groups.filter(name="teacher").exists():
            if group.teacher_id is None or int(user.teacherprofile.user_id) != int(group.teacher_id):
                return Response(status=status.HTTP_403_FORBIDDEN)
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
    def remove_student_from_group(self, request, *args, **kwargs):
        user = self.request.user
        group = self.get_object()
        student_id = kwargs.get('student_id')

        if not user.groups.filter(name="teacher").exists() and not user.groups.filter(name="admin").exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif user.groups.filter(name="teacher").exists():
            if group.teacher_id is None or int(user.teacherprofile.user_id) != int(group.teacher_id):
                return Response(status=status.HTTP_403_FORBIDDEN)
        if student_id is not None and group is not None:
            student = StudentProfile.objects.get(id=student_id)
            group.studentprofile_set.remove(student)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (LanguageAccessPolicy,)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='teacher_id',
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='group_id',
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='student_id',
                type=OpenApiTypes.INT,
            ),
        ],
    ),
)
class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = (LessonAccessPolicy,)

    def get_queryset(self):
        user = self.request.user
        query_params = self.request.query_params
        queryset = Lesson.objects.all()
        if user.groups.filter(name="student").exists():
            queryset = queryset.filter(group__groupmembership__student__user=user)
        elif user.groups.filter(name="teacher").exists():
            queryset = queryset.filter(group__teacher__user=user)
        if teach_id := query_params.get('teacher_id'):
            if user.groups.filter(name="teacher").exists():
                if int(user.teacherprofile.user_id) != int(teach_id):
                    return None
            queryset = queryset.filter(group__teacher_id=teach_id)
        if gr_id := query_params.get('group_id'):
            queryset = queryset.filter(group_id=gr_id)
        if stud_id := query_params.get('student_id'):
            if user.groups.filter(name="student").exists():
                if int(user.studentprofile.user_id) != int(stud_id):
                    return None
            queryset = queryset.filter(group__groupmembership__student_id=stud_id)
        return queryset


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='student_id',
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name='group_id',
                type=OpenApiTypes.INT,
            ),
        ],
    ),
    create=extend_schema(
        request=MarkSerializer,
    ),
    update=extend_schema(
        request=MarkUpdateSerializer,
    ),
)
class MarkViewSet(viewsets.ModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = (MarkAccessPolicy,)

    def get_queryset(self):
        user = self.request.user
        queryset = Mark.objects.all()
        if user.groups.filter(name="student").exists():
            queryset = queryset.filter(group_membership__student__user=user)
        elif user.groups.filter(name="teacher").exists():
            queryset = queryset.filter(group_membership__group__teacher__user=user)
        if stud_id := self.request.query_params.get("student_id"):
            queryset = queryset.filter(group_membership__student_id=stud_id)
        if gr_id := self.request.query_params.get("group_id"):
            queryset = queryset.filter(group_membership__group_id=gr_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return MarkRequestSerializer
        if self.action == 'update':
           return MarkUpdateSerializer
        return MarkSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        gr_id = request.data['group_id']
        st_id = request.data['student_id']
        try:
            if not user.groups.filter(name="teacher").exists() and not user.groups.filter(name="admin").exists():
                return Response(status=status.HTTP_403_FORBIDDEN)
            elif user.groups.filter(name="teacher").exists():
                if int(user.teacherprofile.user_id) != int(Group.objects.get(id=gr_id).teacher_id):
                    return Response(status=status.HTTP_403_FORBIDDEN)
            if gr_id is not None and st_id is not None:

                queryset = GroupMembership.objects.filter(group_id=gr_id)
                gr_mem_id = queryset.get(student_id=st_id).id
        except GroupMembership.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer_class = MarkRequestSerializer(data={'mark': request.data['mark'],
                                                     'description': request.data['description'],
                                                     'group_membership': gr_mem_id})
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    create=extend_schema(
        request=TeacherProfileRequestSerializer,
    ),
    update=extend_schema(
        request=TeacherProfileRequestSerializer,
    ),
)
class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = (TeacherAccessPolicy,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return TeacherProfileRequestSerializer
        elif self.action == 'list':
            return TeacherProfileListSerializer
        return TeacherProfileSerializer


@extend_schema_view(
    create=extend_schema(
        request=AdminProfileRequestSerializer,
    ),
    update=extend_schema(
        request=AdminProfileRequestSerializer,
    ),
)
class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = (AdminAccessPolicy,)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return AdminProfileRequestSerializer
        return AdminProfileSerializer


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='group_id',
                type=OpenApiTypes.INT,
            ),
        ],
    ),
    create=extend_schema(
        request=StudentProfileRequestSerializer,
    ),
    update=extend_schema(
        request=StudentProfileRequestSerializer,
    ),
)
class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = (StudentAccessPolicy,)

    def get_queryset(self):
        gr_id = self.request.query_params.get('group_id')
        if gr_id is not None:
            return StudentProfile.objects.filter(groups__id=gr_id)
        return StudentProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return StudentProfileRequestSerializer
        elif self.action == 'list':
            return StudentProfileListSerializer
        return StudentProfileSerializer
