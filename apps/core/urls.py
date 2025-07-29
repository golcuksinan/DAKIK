from django.urls import path
from .views import HomeViewWithAnnouncementsListing

app_name = 'core'

urlpatterns = [
    path('', HomeViewWithAnnouncementsListing.as_view(), name='home'),
]