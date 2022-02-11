from django.contrib import admin
from .models import Answer, AnswerComment
# Register your models here.
admin.site.register(AnswerComment)
admin.site.register(Answer)