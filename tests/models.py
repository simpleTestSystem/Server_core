from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)


class Theme(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course)


class Document(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()


class Question(models.Model):
    text = models.TextField()
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)


class Option(models.Model):
    text = models.TextField()
    right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

