from django.contrib import admin
from .models import Question, QuestionComment
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionComment)