from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)


class Theme(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='themes')


class Document(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='documents')


class Question(models.Model):
    text = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='questions')


# pretty dirty
# better practice should be storing only link to document and help position
class Help(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    question = models.ForeignKey(Question, related_name='help')


class Option(models.Model):
    text = models.TextField()
    right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')


