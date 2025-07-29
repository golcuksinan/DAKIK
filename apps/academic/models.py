from django.db import models

class University(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default='Turkiye')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Faculties"
        ordering = ['name']
        unique_together = ['code', 'university']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['code', 'faculty']

    def __str__(self):
        return f"{self.name} - {self.faculty.name}"