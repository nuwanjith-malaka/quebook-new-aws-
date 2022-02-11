from django import forms
from .models import Answer, AnswerComment
class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your Answer'}),
        }


class AnswerCommentForm(forms.ModelForm):
    class Meta:
        model = AnswerComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your Comment'}),
        }