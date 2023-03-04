from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from .models import Student, Course, Attendance,Enrollment

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_id', 'course_name')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'time')

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attendance, AttendanceAdmin)
