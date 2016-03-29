from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tests.models import Question, Theme, Course, Document
from tests.serializers import QuestionSerializer, ThemeSerializer, CourseSerializer, DocumentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404


class CourseList(APIView):
    """
    List all courses
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True, context= {'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data, context= {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetail(APIView):
    """
    course detail
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, course_pk, format=None):
        course = self.get_object(course_pk)
        serializer = CourseSerializer(course, context= {'request': request})
        return Response(serializer.data)

    def put(self, request, course_pk, format=None):
        course = self.get_object(course_pk)
        serializer = CourseSerializer(course, data=request.data, context= {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, course_pk, format=None):
        course = self.get_object(course_pk)
        course.delete()


class QuestionList(APIView):
    """
    List all questions or
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    """
    Detailed info about question
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, question_pk, format=None):
        question = self.get_object(question_pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.remove()
        return Response(status=status.HTTP_200_OK)
