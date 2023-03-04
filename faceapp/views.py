# from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, Student, Enrollment
from .forms import CourseForm, DeleteStudentForm, StudentForm, EnrollmentForm

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added succesfully!')
            return redirect('add_student')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def delete_student(request):
    if request.method == 'POST':
        form = DeleteStudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            try:
                student = Student.objects.get(student_id=student_id)
                Enrollment.objects.filter(student=student).delete()
                student.delete()
                messages.success(request, f'Student {student_id} deleted successfully!')
            except Student.DoesNotExist:
                messages.error(request, 'Invalid Student ID!')
            return redirect('delete_student')
    else:
        form = DeleteStudentForm()
    return render(request, 'delete_student.html', {'form': form})


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data['course_id']
            course_name = form.cleaned_data['course_name']
            if Course.objects.filter(course_id=course_id).exists():
                messages.error(request, f'Course with ID {course_id} already exists')
            else:
                course = Course(course_id=course_id, course_name=course_name)
                course.save()
                messages.success(request, f'Course {course_name} added successfully')
                return redirect('courses')
        else:
            messages.error(request, 'Course with this ID already exist. Please try again.')
            return redirect('courses')
    else:
        form = CourseForm()

    context = {'form': form}
    return render(request, 'courses.html', context)

def delete_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)

    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course "{course.course_name}" deleted successfully!')
        return redirect('courses')

    return render(request, 'courses.html', {'course': course})

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from .models import Course, Student, Enrollment
from .forms import CourseForm

def edit_course(request, course_id):
    course = get_object_or_404(Course, course_id=course_id)
    students = Student.objects.filter(enrollment__course=course)
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                enrollment, created = Enrollment.objects.get_or_create(course=course, student=student)
                if created:
                    messages.success(request, f'{student} enrolled successfully in {course} course.')
                else:
                    messages.warning(request, f'{student} is already enrolled in {course} course.')
            except Student.DoesNotExist:
                messages.error(request, f'Student with ID {student_id} does not exist.')
        return redirect(reverse('edit_course', kwargs={'course_id': course_id}))
        
    context = {
        'course': course,
        'students': students,
    }
    return render(request, 'edit_course.html', context)
