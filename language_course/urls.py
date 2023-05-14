from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('register/', TemplateView.as_view(template_name="register.html")),
    path('confirmation-register/', TemplateView.as_view(template_name="confirmation-register.html")),
    path('profile/<int:id>', TemplateView.as_view(template_name="profile.html")),
    path('profile/me', TemplateView.as_view(template_name="profile.html")),
    path('groups/', TemplateView.as_view(template_name="lists.html")),
    path('groups/<int:group_id>/', TemplateView.as_view(template_name="lists.html")),
    path('groups/<int:group_id>/<int:student_id>/', TemplateView.as_view(template_name="lists.html")),
    path('groups/<int:group_id>/<int:student_id>/<int:mark_id>/', TemplateView.as_view(template_name="mark-form.html")),
    path('groups/<int:group_id>/<int:student_id>/add-mark/', TemplateView.as_view(template_name="mark-form.html")),
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('admin/', admin.site.urls),
    path('api/', include('course.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
