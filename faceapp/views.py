# from pyexpat.errors import messages
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Course, Student, Enrollment,Attendance
from .forms import CourseForm, DeleteStudentForm, StudentForm, EnrollmentForm

from django.shortcuts import render
from .models import Course, Student

def home(request):
    selected_course = request.GET.get('course_id')

    if selected_course:
        selected_course = selected_course
        selected_course_name = Course.objects.get(course_id=selected_course).course_name
        students = Student.objects.filter(enrollment__course=selected_course)
    else:
        selected_course_name = None
        students = None

    courses = Course.objects.all()
    context = {
        'courses': courses,
        'selected_course': selected_course,
        'selected_course_name': selected_course_name,
        'students': students,
    }
    return render(request, 'home.html', context)



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
        else:
            enrollment_id = request.POST.get('enrollment_id')
            if enrollment_id:
                try:
                    enrollment = Enrollment.objects.get(id=enrollment_id, course=course)
                    student = enrollment.student
                    enrollment.delete()
                    messages.success(request, f'{student} unenrolled successfully from {course} course.')
                except Enrollment.DoesNotExist:
                    messages.error(request, 'Invalid enrollment ID')
            else:
                return HttpResponseBadRequest()
        return redirect(reverse('edit_course', kwargs={'course_id': course_id}))
        
    context = {
        'course': course,
        'students': students,
    }
    return render(request, 'edit_course.html', context)

def unenroll_student(request, course_id, student_id):
    course = get_object_or_404(Course, course_id=course_id)
    student = get_object_or_404(Student, student_id=student_id)
    
    try:
        enrollment = Enrollment.objects.get(course=course, student=student)
        enrollment.delete()
        messages.success(request, f'Student {student} unenrolled from {course}.')
    except Enrollment.DoesNotExist:
        messages.warning(request, f'Student {student} is not enrolled in {course}.')
        
    return redirect(reverse('edit_course', kwargs={'course_id': course_id}))
