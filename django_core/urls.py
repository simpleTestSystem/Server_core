"""django_core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers, viewsets
from tests.serializers import CourseSerializer, DocumentSerializer, ThemeSerializer, QuestionSerializer, OptionSerializer, HelpSerializer, CourseHyperlinkSerializer, ThemeHyperlinkSerializer
from tests.models import Course, Document, Theme, Question, Option, Help
from rest_framework.response import Response


# ViewSets define the view behavior.
class CourseViewSet(viewsets.ModelViewSet):

    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseHyperlinkSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ThemeViewSet(viewsets.ModelViewSet):

    def list(self, request):
        queryset = Theme.objects.all()
        serializer = ThemeHyperlinkSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)

    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'themes', ThemeViewSet)
router.register(r'questions', QuestionViewSet)


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^api/', include('rest_framework.urls', namespace='rest_framework'))
]
