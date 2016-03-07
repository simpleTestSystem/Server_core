from tests.models import Theme, Question, Option, Course, Document, Help
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class OptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Option
        fields = ('right', 'text')


class HelpSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Help
        fields = ('name', 'content')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    options = OptionSerializer(many=True)
    # TODO replace many value to false (seems like many=false require any help for question)
    help = HelpSerializer(many=True)

    class Meta:
        model = Question
        fields = ('text', 'help', 'options')


class ThemeSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Theme
        fields = ('name', 'questions')


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'content')


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    themes = ThemeSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'documents', 'themes')

