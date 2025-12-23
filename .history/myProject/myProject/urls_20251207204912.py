"""
URL configuration for myProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from basic.views import sample
from basic.views import sample1
from basic.views import sampleInfo
from basic.views import dynamicResponse
from basic.views import add, sub, mul, div, health, add_student, check, login, getAllUsers, home, aboutus, welcome
from basic.views import get_all_students, get_student_by_id, filter_students_age_gte_20,  filter_students_age_lte_25, get_unique_ages, count_total_students
from basic.views import job1,job2,signUp
from basic import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('greet/',sample),
    path('53r54r/',sample1),
    path('info/',sampleInfo),
    path('name/',dynamicResponse),
    path('add/', add),
    path('sub/', sub),
    path('mul/', mul),
    path('div/', div),
    path('health/',health),
    path('add_stu/',add_student),
    path('job1/',job1),
    path('job2/',job2),
    path('check/',check),
    path('login/',login),
    path('getallusers/',getAllUsers),
    path("signup/", views.signUp),
    path("get-users/", views.getUsers),
    path("delete-user/<int:id>/", views.deleteUser),
    path('home/',home,name="home"),
    path('aboutus/',aboutus,name="about"),
    path('welcome/',welcome,name="welcome"),
    path('contact',welcome,name="contact"),
    path('services',welcome,name="services"),
    path('products',we ,name=""),
   

    path('students/', get_all_students, name='get_all_students'),
    path('student/<int:id>/', get_student_by_id, name='get_student_by_id'),
    path('students/age_gte_20/', filter_students_age_gte_20, name='filter_students_age_gte_20'),
    path('students/age_lte_25/', filter_students_age_lte_25, name='filter_students_age_lte_25'),
    path('students/unique_ages/', get_unique_ages, name='get_unique_ages'),
    path('students/count/', count_total_students, name='count_total_students'),
]
