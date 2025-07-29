from django.db import models
from academic.models import Department
from accounts.models import Student
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    is_elective = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        unique_together = ['code', 'department']

    def __str__(self):
        return f"{self.code} - {self.name}"


class CourseRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    SEMESTER_CHOICES = [
        ('fall', 'Fall'),
        ('spring', 'Spring'),
        ('summer', 'Summer'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='course_requests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    academic_year = models.IntegerField(
        validators=[MinValueValidator(2020), MaxValueValidator(2050)]
    )
    request_message = models.TextField(blank=True)
    admin_response = models.TextField(blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)
    responded_by = models.ForeignKey(
        Student, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='course_request_responses'
    )

    class Meta:
        ordering = ['-requested_at']
        unique_together = ['student', 'course', 'semester', 'academic_year']

    def __str__(self):
        return f"{self.student.student_number} - {self.course.code} ({self.status})"

    def save(self, *args, **kwargs):
        if self.status in ['approved', 'rejected'] and not self.responded_at:
            self.responded_at = timezone.now()
        super().save(*args, **kwargs)


class StudentCourse(models.Model):
    SEMESTER_CHOICES = [
        ('fall', 'Güz'),
        ('spring', 'Bahar'),
        ('summer', 'Yaz'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolled_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    academic_year = models.IntegerField(
        validators=[MinValueValidator(2020), MaxValueValidator(2050)]
    )
    grade_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-academic_year', '-semester']
        unique_together = ['student', 'course', 'semester', 'academic_year']

    def __str__(self):
        return f"{self.student.student_number} - {self.course.code} ({self.academic_year} {self.semester})"