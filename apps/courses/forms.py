from django import forms
from django.db import models
from .models import Course
from academic.models import Department

class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'is_elective', 'description']
        labels = {
            'name': 'Ders Adı',
            'code': 'Ders Kodu',
            'is_elective': 'Seçmeli Mi',
            'description': 'Açıklama'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)