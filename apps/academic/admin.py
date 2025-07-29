from django.contrib import admin
from .models import University, Faculty, Department

class UniversityAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        # UniversityAdmin kendi üniversitesindeki tüm fakülteleri ve bölümleri görebilmeli
        if user.groups.filter(name='University Administrator').exists():
            if hasattr(qs.model, 'university'):
                return qs.filter(university=user.university)
            return qs.filter(id=user.university.id)
        return qs.none()

class FacultyAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        # UniversityAdmin kendi üniversitesindeki tüm fakülteleri görebilmeli
        if user.groups.filter(name='University Administrator').exists():
            if hasattr(qs.model, 'university'):
                return qs.filter(university=user.university)
        # FacultyAdmin kendi fakültesindeki tüm bölümleri görebilmeli
        if user.groups.filter(name='Faculty Administrator').exists():
            if hasattr(qs.model, 'faculty'):
                return qs.filter(faculty=user.faculty)
            return qs.filter(id=user.faculty.id)
        return qs.none()

class DepartmentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        # UniversityAdmin kendi üniversitesindeki tüm departmanları görebilmeli
        if user.groups.filter(name='University Administrator').exists():
            if hasattr(qs.model, 'faculty'):
                return qs.filter(faculty__university=user.university)
        # FacultyAdmin kendi fakültesindeki tüm departmanları görebilmeli
        if user.groups.filter(name='Faculty Administrator').exists():
            if hasattr(qs.model, 'faculty'):
                return qs.filter(faculty=user.faculty)
        # DepartmentAdmin sadece kendi departmanını görebilir
        if user.groups.filter(name='Department Administrator').exists():
            if hasattr(qs.model, 'department'):
                return qs.filter(department=user.department)
            return qs.filter(id=user.department.id)
        return qs.none()

admin.site.register(University, UniversityAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department, DepartmentAdmin)
