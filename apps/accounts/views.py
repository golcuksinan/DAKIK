from django.http import JsonResponse
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import StudentRegistrationForm, StudentUpdateForm
from accounts.models import Student
from academic.models import University, Faculty, Department

def load_faculties(request):
    university_id = request.GET.get('university')
    faculties = Faculty.objects.filter(university_id=university_id).values('id', 'name')
    return JsonResponse(list(faculties), safe=False)

def load_departments(request):
    faculty_id = request.GET.get('faculty')
    departments = Department.objects.filter(faculty_id=faculty_id).values('id', 'name')
    return JsonResponse(list(departments), safe=False)


class StudentCreateView(CreateView):
    template_name = 'accounts/register.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['universities'] = University.objects.all()
        return context

class StudentProfileView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'accounts/profile.html'

    def get_object(self):
        return self.request.user

class StudentProfileEditView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)