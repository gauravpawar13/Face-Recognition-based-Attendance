from django.db import models
import os
import json

# Create your models here.

class Student(models.Model):
    student_id = models.CharField(primary_key=True, unique=True, max_length=20)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photos/')

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete all associated data before deleting student
        Attendance.objects.filter(student=self).delete()
        Enrollment.objects.filter(student=self).delete()

        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        # Call the default delete method
        super().delete(*args, **kwargs)
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    
class Course(models.Model):
    course_id = models.CharField(primary_key=True, unique=True, max_length=20)
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name
    
    def delete(self, *args, **kwargs):
        # Delete all associated data before deleting student
        Attendance.objects.filter(course=self).delete()
        Enrollment.objects.filter(course=self).delete()
        # Call the default delete method
        super().delete(*args, **kwargs)
    
class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


