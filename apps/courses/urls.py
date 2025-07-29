from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseListView.as_view(), name='course-list'),
    path('add/', views.CourseAddView.as_view(), name='course-add'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    #path('request/', views.CourseRequestView.as_view(), name='course-request'),
]