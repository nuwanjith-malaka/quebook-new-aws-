from django import forms
from user.models import AskerProfile

class AskerProfileForm(forms.ModelForm):
    class Meta:
        model = AskerProfile
        exclude = ['user']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Photo'}),
            'school': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'}),
            'grade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grade'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
        }