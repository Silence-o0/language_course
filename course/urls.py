from django.urls import path
from course import views

urlpatterns = [
    path('course/', views.LangList.as_view()),
]