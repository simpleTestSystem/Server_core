from tests.models import Theme, Question, Option, Course, Document, Help
from rest_framework import routers, serializers, viewsets


# Serializers define the API representation.
class OptionCoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('right', 'text')


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ('right', 'text', 'question')


class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ('question', 'name', 'content')


class HelpCoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ('name', 'content')


class QuestionHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('url', 'text')


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionCoreSerializer(many=True)
    # TODO replace many value to false (seems like many=false require any help for question)
    help = HelpCoreSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'help', 'options', 'theme')

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
        if 'theme' in validated_data:
            question = Question.objects.create(text=validated_data['text'], theme=validated_data['theme'])
        else:
            raise serializers.ValidationError({ 'error':'question should be part of theme'})

        for option_data in validated_data['options']:
            option_data['question'] = question.id
            serializer = OptionSerializer(data=option_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)
            serializer.save()

        for help_data in validated_data['help']:
            help_data['question'] = question.id
            serializer = HelpSerializer(data=help_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)
            serializer.save()

        question.save()
        return question


class QuestionCoreSerializer(QuestionSerializer):
    class Meta:
        model = Question
        fields = ('text', 'help', 'options')


class ThemeHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ('name', 'url')


class ThemeSerializer(serializers.ModelSerializer):
    questions = QuestionCoreSerializer(many=True)

    class Meta:
        model = Theme
        fields = ('name', 'course', 'questions')

    def create(self, validated_data):
        theme = Theme.objects.create(name=validated_data['name'], course=validated_data['course'])
        theme.save()
        for question_data in validated_data['questions']:
            question_data['theme'] = theme.id
            serializer = QuestionSerializer(data=question_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)
        return theme


class ThemeCoreSerializer(ThemeSerializer):
    class Meta:
        model = Theme
        fields = ('name', 'questions')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'content')


class CourseHyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'url')


class CourseHyperlinkInfoSerializer(serializers.ModelSerializer):
    themes = ThemeHyperlinkSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'documents', 'themes')
        depth = 1


class CourseSerializer(serializers.ModelSerializer):
    themes = ThemeCoreSerializer(many=True)
    documents = DocumentSerializer(many=True)

    class Meta:
        model = Course
        fields = ('name', 'documents', 'themes')

    def create(self, validated_data):
        course = Course.objects.create(name=validated_data['name'])

        for theme_data in validated_data['themes']:
            theme_data['course'] = course.id
            serializer = ThemeSerializer(data=theme_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise serializers.ValidationError(serializer.errors)

        course.save()
        return course

