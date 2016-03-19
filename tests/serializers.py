from tests.models import Theme, Question, Option, Course, Document, Help
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('right', 'text')


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ('name', 'content')


class QuestionHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('url', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    # TODO replace many value to false (seems like many=false require any help for question)
    help = HelpSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'help', 'options',('theme'))

    def create(self, validated_data):
        if len(validated_data['options']) < 2:
            raise serializers.ValidationError('you need to send at least 2 options for question')
        """
        same_questions = Question.objects.filter(text=validated_data['text'])

        if len(same_questions) > 0:
            for same_question in same_questions:
                raise serializers.ValidationError({
                    'text' : 'you can not add same question in system, please update existing',
                    'id' : same_question.id})
        """
        print(validated_data)
        if ('theme' in validated_data):
            question = Question.objects.create(text=validated_data['text'], theme=validated_data['theme'])
        else:
            raise serializers.ValidationError({ 'error':'question should be part of theme',
                                                'text': validated_data['text']})

        for option_data in validated_data['options']:
            serializer = OptionSerializer(data=option_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)

            option = Option.objects.create(text=option_data['text'], right=option_data['right'], question=question)

        return question


class ThemeHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('name', 'url')


class ThemeSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Theme
        fields = ('name', 'course', 'questions')

    def create(self, validated_data):
        serializers.ValidationError('fuck yoyu')
        theme = Theme.objects.create(name=validated_data['name'], course=validated_data['course'])
        for question_data in validated_data['questions']:
            print(question_data)
            question_data['theme'] = 1
            print(question_data)
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid():
                serializer.save()
            else:
                serializers.ValidationError('=(')
        return theme

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'content')


class CourseHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'url')


class CourseSerializer(serializers.ModelSerializer):
    themes = ThemeHyperlinkSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'documents', 'themes')
        depth = 1

