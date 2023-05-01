from django.urls import path, include
from course import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'languages', views.LanguageViewSet, basename="language")
router.register(r'groups', views.GroupViewSet, basename="group")
router.register(r'lessons', views.LessonViewSet, basename="lesson")
router.register(r'marks', views.MarkViewSet, basename="mark")
router.register(r'teacher_profiles', views.TeacherProfileViewSet, basename="teacher_profile")
router.register(r'admin_profiles', views.AdminProfileViewSet, basename="admin_profile")
router.register(r'student_profiles', views.StudentProfileViewSet, basename="student_profile")

urlpatterns = [
    path('', include(router.urls)),
]
