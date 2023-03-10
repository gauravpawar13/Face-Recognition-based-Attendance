# importing req libraries

from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import serializers
from django.urls import reverse

from .models import Course, Student, Enrollment
from .forms import CourseForm, DeleteStudentForm, StudentForm

import cv2
import numpy as np
import face_recognition

# Create your views here.


def home(request):
    """This handles the data of the two boxes on home page."""
    selected_course = request.GET.get("course_id")

    if selected_course:
        selected_course = selected_course
        selected_course_name = Course.objects.get(course_id=selected_course).course_name
        students = Student.objects.filter(enrollment__course=selected_course)
    else:
        selected_course_name = None
        students = None

    courses = Course.objects.all()
    context = {
        "courses": courses,
        "selected_course": selected_course,
        "selected_course_name": selected_course_name,
        "students": students,
    }
    return render(request, "home.html", context)


def take_attendance(request):
    """This function implements the face recognition algorithm"""

    def Encodings(images):
        """It will return the encoded images of images passed into this function"""
        encodeList = []
        for img in images:
            img = cv2.cvtColor(
                img, cv2.COLOR_BGR2RGB
            )  # converting image of bgr format to rgb
            encode = face_recognition.face_encodings(img)[0]  # encoding of image
            encodeList.append(encode)
        return encodeList

    if request.method == "POST":
        # Start the attendance

        if request.POST.get("action") == "start":
            path = "student_photos"  # place where images are stored
            images = []  # images in the place
            classNames = []  # names of images
            namelist = []

            course_id = request.POST.get("course_id")
            mylist = Student.objects.filter(enrollment__course=course_id)  # req images

            for cls in mylist:
                current_image = cv2.imread(f"{cls.photo}")
                images.append(current_image)
                classNames.append(cls.name)

            # print("Got the Class details")

            encoded_list = Encodings(images)
            # print("Encoded images")

            webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # to get camera view

            if not webcam.isOpened():
                return JsonResponse(
                    {"success": False, "message": "Failed to open camera."}
                )

            while True:
                successful_frame_read, frame = webcam.read()
                if successful_frame_read:
                    sized_image = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
                    sized_image = cv2.cvtColor(sized_image, cv2.COLOR_BGR2RGB)

                    faceloc = face_recognition.face_locations(sized_image)
                    encodedface = face_recognition.face_encodings(sized_image, faceloc)

                    if encoded_list:
                        # for comparing the faces with previously loaded data
                        for encodeofface, locofface in zip(encodedface, faceloc):
                            matches = face_recognition.compare_faces(
                                encoded_list, encodeofface
                            )
                            if len(matches) == 0:  # no matches found for current face
                                continue  # skip to next face
                            facedis = face_recognition.face_distance(
                                encoded_list, encodeofface
                            )
                            matchindex = np.argmin(facedis)

                            if matches[matchindex]:
                                name = classNames[matchindex]
                                # print(name)
                                y1, x2, y2, x1 = locofface
                                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                                cv2.rectangle(
                                    frame,
                                    (x1, y2 - 35),
                                    (x2, y2),
                                    (0, 255, 0),
                                    cv2.FILLED,
                                )
                                cv2.putText(
                                    frame,
                                    str(name),
                                    (x1 + 6, y2 - 6),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    1,
                                    (255, 255, 255),
                                    2,
                                )
                                if (
                                    name not in namelist
                                ):  # so that one student one entry
                                    namelist.append(name)

                    cv2.imshow("webcam", frame)

                    key = cv2.waitKey(1)  # for taking a key as input
                    if (
                        key == 81 or key == 113
                    ):  # for quiting the task by pressing q or Q
                        break
            # print(namelist)

            webcam.release()
            cv2.destroyAllWindows()

            pres_stud = Student.objects.filter(name__in=namelist)
            data = serializers.serialize(
                "json", pres_stud, fields=("name", "student_id")
            )

            return JsonResponse(data, safe=False)
    return render(request, "home.html")


def add_student(request):
    """Inserting Student into database, the id must be unique"""
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student added succesfully!")
            return redirect("add_student")
    else:
        form = StudentForm()
    return render(request, "add_student.html", {"form": form})


def delete_student(request):
    """Removes student from everywhere"""
    if request.method == "POST":
        form = DeleteStudentForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data["student_id"]
            try:
                student = Student.objects.get(student_id=student_id)
                Enrollment.objects.filter(student=student).delete()
                student.delete()
                messages.success(request, f"Student {student_id} deleted successfully!")
            except Student.DoesNotExist:
                messages.error(request, "Invalid Student ID!")
            return redirect("delete_student")
    else:
        form = DeleteStudentForm()
    return render(request, "delete_student.html", {"form": form})


def courses(request):
    """Shows the courses created"""
    courses = Course.objects.all()
    return render(request, "courses.html", {"courses": courses})


def add_course(request):
    """Adding a new course, the id must be unique"""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course_id = form.cleaned_data["course_id"]
            course_name = form.cleaned_data["course_name"]
            if Course.objects.filter(course_id=course_id).exists():
                messages.error(request, f"Course with ID {course_id} already exists")
            else:
                course = Course(course_id=course_id, course_name=course_name)
                course.save()
                messages.success(request, f"Course {course_name} added successfully")
                return redirect("courses")
        else:
            messages.error(
                request, "Course with this ID already exist. Please try again."
            )
            return redirect("courses")
    else:
        form = CourseForm()

    context = {"form": form}
    return render(request, "courses.html", context)


def delete_course(request, course_id):
    """Removes the course and data associated with it"""
    course = get_object_or_404(Course, course_id=course_id)

    if request.method == "POST":
        course.delete()
        messages.success(
            request, f'Course "{course.course_name}" deleted successfully!'
        )
        return redirect("courses")

    return render(request, "courses.html", {"course": course})


def edit_course(request, course_id):
    """To add a student or to remove"""
    course = get_object_or_404(Course, course_id=course_id)
    students = Student.objects.filter(enrollment__course=course)

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        if student_id:
            try:
                student = Student.objects.get(student_id=student_id)
                enrollment, created = Enrollment.objects.get_or_create(
                    course=course, student=student
                )
                if created:
                    messages.success(
                        request, f"{student} enrolled successfully in {course} course."
                    )
                else:
                    messages.warning(
                        request, f"{student} is already enrolled in {course} course."
                    )
            except Student.DoesNotExist:
                messages.error(request, f"Student with ID {student_id} does not exist.")
        else:
            enrollment_id = request.POST.get("enrollment_id")
            if enrollment_id:
                try:
                    enrollment = Enrollment.objects.get(id=enrollment_id, course=course)
                    student = enrollment.student
                    enrollment.delete()
                    messages.success(
                        request,
                        f"{student} unenrolled successfully from {course} course.",
                    )
                except Enrollment.DoesNotExist:
                    messages.error(request, "Invalid enrollment ID")
            else:
                return HttpResponseBadRequest()
        return redirect(reverse("edit_course", kwargs={"course_id": course_id}))

    context = {
        "course": course,
        "students": students,
    }
    return render(request, "edit_course.html", context)


def unenroll_student(request, course_id, student_id):
    """Removes student from that respective course"""
    course = get_object_or_404(Course, course_id=course_id)
    student = get_object_or_404(Student, student_id=student_id)

    try:
        enrollment = Enrollment.objects.get(course=course, student=student)
        enrollment.delete()
        messages.success(request, f"Student {student} unenrolled from {course}.")
    except Enrollment.DoesNotExist:
        messages.warning(request, f"Student {student} is not enrolled in {course}.")

    return redirect(reverse("edit_course", kwargs={"course_id": course_id}))
