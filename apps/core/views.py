from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from announcements.models import Announcement

class HomeViewWithAnnouncementsListing(LoginRequiredMixin, ListView):
    model = Announcement
    template_name = 'home.html'
    context_object_name = 'announcements'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'university') or not hasattr(user, 'faculty') or not hasattr(user, 'department'):
            return Announcement.objects.none()

        return Announcement.objects.filter(
            Q(target_type='university', target_id=user.university.id) |
            Q(target_type='faculty', target_id=user.faculty.id) |
            Q(target_type='department', target_id=user.department.id),
            is_active=True,
            publish_date__lte=timezone.now()
        )