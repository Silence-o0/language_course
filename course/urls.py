from django.urls import path, include
from rest_framework_nested import routers

from course import views

router = routers.SimpleRouter()
router.register(r'languages', views.LanguageViewSet, basename="language")
router.register(r'groups', views.GroupViewSet, basename="group")
router.register(r'lessons', views.LessonViewSet, basename="lesson")
router.register(r'marks', views.MarkViewSet, basename="mark")
router.register(r'teachers', views.TeacherProfileViewSet, basename="teacher_profile")
router.register(r'admins', views.AdminProfileViewSet, basename="admin_profile")
router.register(r'students', views.StudentProfileViewSet, basename="student_profile")


urlpatterns = [
    path('', include(router.urls)),
]
