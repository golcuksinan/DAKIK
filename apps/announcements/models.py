import os
from django.db import models
from django.utils import timezone
from accounts.models import Student
from academic.models import University, Faculty, Department

def upload_announcement_attachment(instance, filename):
    """Generate upload path for announcement attachments"""
    return f'announcements/{instance.announcement.id}/{filename}'

class Announcement(models.Model):
    TARGET_CHOICES = [
        ('university', 'Üniversite Duyurusu'),
        ('faculty', 'Fakülte Duyurusu'),
        ('department', 'Bölüm Duyurusu'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    target_type = models.CharField(max_length=15, choices=TARGET_CHOICES)
    target_id = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(Student, on_delete=models.SET_NULL, related_name='announcements', null=True)
    is_active = models.BooleanField(default=True)
    publish_date = models.DateTimeField(default=timezone.now)
    expire_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publish_date']

    def __str__(self):
        return f"{self.title} ({self.target_type})"

    def is_expired(self):
        """Check if announcement is expired"""
        if self.expire_date:
            return timezone.now() > self.expire_date
        return False

    def get_target_object(self):
        """Get the actual target object (University, Faculty, or Department)"""
        if self.target_type == 'university':
            return University.objects.get(id=self.target_id)
        elif self.target_type == 'faculty':
            return Faculty.objects.get(id=self.target_id)
        elif self.target_type == 'department':
            return Department.objects.get(id=self.target_id)
        return None

class AnnouncementAttachment(models.Model):
    announcement = models.ForeignKey(
        Announcement, 
        on_delete=models.CASCADE, 
        related_name='attachments'
    )
    file_name = models.CharField(max_length=255)
    file_path = models.FileField(upload_to=upload_announcement_attachment)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['file_name']

    def __str__(self):
        return f"{self.announcement.title} - {self.file_name}"

    def save(self, *args, **kwargs):
        if self.file_path:
            self.file_size = self.file_path.size
            if not self.file_name:
                self.file_name = os.path.basename(self.file_path.name)
        super().save(*args, **kwargs)