from django.db import models
from django.contrib.auth.models import AbstractUser
from academic.models import University, Faculty, Department
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Student(AbstractUser):
    GRADE_CHOICES = [
        (1, '1. Sınıf'),
        (2, '2. Sınıf'),
        (3, '3. Sınıf'),
        (4, '4. Sınıf'),
        (5, '5. Sınıf'),
        (6, '6. Sınıf'),
    ]
    student_number = models.CharField(max_length=20, null=True, blank=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='students', default=1)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students', default=1)
    current_grade = models.IntegerField(
        choices=GRADE_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')
    enrollment_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_number']

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        # Ensure faculty belongs to the selected university
        if self.faculty.university != self.university:
            raise ValueError("Faculty must belong to the selected university")
        # Ensure department belongs to the selected faculty
        if self.department.faculty != self.faculty:
            raise ValueError("Department must belong to the selected faculty")
        super().save(*args, **kwargs)