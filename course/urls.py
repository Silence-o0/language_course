from django.urls import path, include
from course import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'language', views.LanguageViewSet, basename="language")
router.register(r'group', views.GroupViewSet, basename="group")
router.register(r'lesson', views.LessonViewSet, basename="lesson")
router.register(r'mark', views.MarkViewSet, basename="mark")
router.register(r'teacher_profile', views.TeacherProfileViewSet, basename="teacher_profile")
router.register(r'admin_profile', views.AdminProfileViewSet, basename="admin_profile")
router.register(r'student_profile', views.StudentProfileViewSet, basename="student_profile")


urlpatterns = [
    path('', include(router.urls)),
]
