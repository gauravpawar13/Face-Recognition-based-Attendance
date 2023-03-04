"""facepro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from faceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('add_student/', views.add_student, name='add_student'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('courses/', views.courses, name='courses'),
    path('add_course/', views.add_course, name='add_course'),
    path('edit_course/<str:course_id>/', views.edit_course, name='edit_course'),
    path('delete_course/<str:course_id>/', views.delete_course, name='delete_course'),
]
