from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import *

from language_course.serializers import *


class LangList(APIView):
    def get(self, request, format=None):
        lang = Language.objects.all()
        serializer = LanguageSerializer(lang, many=True)
        return Response(serializer.data)


