from django.urls import path
from .views import AdmissionListCreateAPIView, AdmissionDetailAPIView, course_options_view

urlpatterns = [
    path('', AdmissionListCreateAPIView.as_view(), name='admission-list-create'),
    path('<int:pk>/', AdmissionDetailAPIView.as_view(), name='admission-detail'),
    path('courses/filter/', course_options_view, name='course-filter'),
]
