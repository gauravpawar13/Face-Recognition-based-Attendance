from django import forms
from .models import Course,Student,Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'photo']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']

class DeleteStudentForm(forms.Form):
    student_id = forms.CharField(label='Student ID', max_length=20)
