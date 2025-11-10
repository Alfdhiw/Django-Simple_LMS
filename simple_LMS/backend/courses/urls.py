# courses/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL untuk /courses/
    path('', views.course_list, name='course_list'), 
]