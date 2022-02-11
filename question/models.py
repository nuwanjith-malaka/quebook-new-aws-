from cProfile import label
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.urls import reverse
# Create your models here.
TAG = [
    ('Buddhism', 'Buddhism'),
    ('Sinhala', 'Sinhala'),
    ('English', 'English'),
    ('Mathematics', 'Mathematics'),
    ('Geography', 'Geography'),
    ('Science', 'Science'),
    ('Commerce', 'Commerce'),
    ('Agriculture', 'Agriculture'),
    ('ICT', 'ICT'),
    ('Drama', 'Drama'),
    ('Art', 'Art'),
    ('Dance', 'Dance'),
    ('History', 'History'),
    ('Music', 'Music'),
    ('Health', 'Health'),
    ('Tamil', 'Tamil'),
]

class Question(models.Model):
    heading = models.CharField(max_length=100, null=True, blank=True)
    tag = models.CharField(
        max_length=15,
        choices=TAG,
        default='Buddhism',
    )
    body = TextField(verbose_name='', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('question_single', kwargs={'pk': self.pk})

class QuestionComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)