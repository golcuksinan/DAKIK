from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Student
from academic.models import Faculty, Department

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = Student
        fields = [
            'username',
            'email',
            'university',
            'faculty',
            'department',
            'current_grade',
            'password1',
            'password2'
        ]
        labels = {
            'username': 'Kullanıcı Adı',
            'email': 'E-posta',
            'university': 'Üniversite',
            'faculty': 'Fakülte',
            'department': 'Bölüm',
            'current_grade': 'Mevcut Sınıf',
            'password1': 'Şifre',
            'password2': 'Şifre (Tekrar)',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Başlangıçta fakülte ve bölüm seçenekleri boş olsun
        self.fields['faculty'].queryset = Faculty.objects.none()
        self.fields['department'].queryset = Department.objects.none()

        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['faculty'].queryset = Faculty.objects.filter(university_id=university_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset

        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['department'].queryset = Department.objects.filter(faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                pass

class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'current_grade']
    