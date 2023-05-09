from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('login/', TemplateView.as_view(template_name="login.html")),
    path('register/', TemplateView.as_view(template_name="register.html")),
    path('reset-password/', TemplateView.as_view(template_name="reset-password.html")),
    path('confirmation/', TemplateView.as_view(template_name="confirmation.html")),
    path('admin/', admin.site.urls),
    path('api/', include('course.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
