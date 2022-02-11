from django.contrib import admin
from .models import AnswerDownVote,AnswerUpVote, QuestionDownVote,QuestionUpVote
# Register your models here.
admin.site.register(AnswerDownVote)
admin.site.register(AnswerUpVote)
admin.site.register(QuestionUpVote)
admin.site.register(QuestionDownVote)