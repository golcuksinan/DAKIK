from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Course, StudentCourse, CourseRequest
from .forms import CourseAddForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from accounts.models import Student
from django.shortcuts import get_object_or_404

class CourseListView(LoginRequiredMixin, ListView):
    model = StudentCourse
    template_name = 'courses/mycourses.html'
    context_object_name = 'student_courses'
    
    def get_queryset(self):
        try:
            # Since Student is a custom user model, self.request.user is already a Student instance
            return StudentCourse.objects.filter(
                student=self.request.user
            ).select_related('course', 'course__department').order_by('-academic_year', '-semester')
        except Exception:
            return StudentCourse.objects.none()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add available courses that the student can request
        student = self.request.user
        context['available_courses'] = Course.objects.filter(
            Q(department=student.department) | Q(is_elective=True)
        ).exclude(
            enrolled_students__student=student,
            enrolled_students__is_active=True
        ).order_by('code')
        return context

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        
        # Get related courses from the same department
        context['related_courses'] = Course.objects.filter(
            department=self.object.department
        ).exclude(id=self.object.id)[:5]  # Limit to 5 related courses
        
        # Get student's enrollment status for this course
        try:
            context['enrollment'] = StudentCourse.objects.get(
                student=student,
                course=self.object,
                is_active=True
            )
        except StudentCourse.DoesNotExist:
            context['enrollment'] = None
            
        # Get any pending course requests
        try:
            context['course_request'] = CourseRequest.objects.get(
                student=student,
                course=self.object,
                status='pending'
            )
        except CourseRequest.DoesNotExist:
            context['course_request'] = None
            
        return context
    
class CourseAddView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Course
    form_class = CourseAddForm
    template_name = 'courses/course_add.html'
    success_url = reverse_lazy('course-list')
    success_message = "%(name)s dersi başarıyla oluşturuldu"

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.department = self.request.user.department
        return super().form_valid(form)


 