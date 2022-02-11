from django.db import models
from django.contrib.auth.models import User
from question.models import Question
# Create your models here.
class Answer(models.Model):
    body = models.TextField('Answer')
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

class AnswerComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)