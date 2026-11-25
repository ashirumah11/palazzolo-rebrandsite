"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
import os

from content.views import home_view, about_view, event_list_view, event_detail_view, gallery_list_view
from contacts.views import contact_view
from courses.views import course_list_view, course_detail_view, department_detail_view
from admissions.views import admission_apply_view, admission_track_view, course_options_view, fees_list_view, admission_requirements_view, admission_procedures_view
from news.views import news_list_view, news_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('courses/', course_list_view, name='course_list'),
    path('courses/<slug:slug>/', course_detail_view, name='course_detail'),
    path('departments/<slug:slug>/', department_detail_view, name='department_detail'),
    path('admissions/', admission_procedures_view, name='admissions'),
    path('admissions/apply/', admission_apply_view, name='admission_apply'),
    path('admissions/track/', admission_track_view, name='admission_track'),
    path('admissions/courses/filter/', course_options_view, name='course_filter'),
    path('admissions/requirements/', admission_requirements_view, name='admission_requirements'),
    path('admissions/procedures/', admission_procedures_view, name='admission_procedures'),
    path('news/', news_list_view, name='news_list'),
    path('news/<slug:slug>/', news_detail_view, name='news_detail'),
    path('events/', event_list_view, name='event_list'),
    path('events/<int:pk>/', event_detail_view, name='event_detail'),
    path('gallery/', gallery_list_view, name='gallery_list'),
    path('fees/', fees_list_view, name='fees_list'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('config.api_urls')),
    # Resilient media route ensuring uploaded institutional assets always resolve
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)