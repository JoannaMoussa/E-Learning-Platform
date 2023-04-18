from django.test import TestCase
from .models import User, Course


class NetworkTestCase(TestCase):

    def setUp(self):

        # Create instructors
        instructors_metadata = [("Joseph", "Python Instructor"),
                                ("Joanna", "Web development Instructor")]
        instructors = []
        for i, (fname, title) in enumerate(instructors_metadata):
            instructor = User.objects.create(
                id=i+1, email=f"{fname}@example.com", first_name=fname, role=User.INSTRUCTOR,
                instructor_title=title, username=fname,
                about=f"About {fname}")
            instructors.append(instructor)

        # Create courses
        courses_metadata = [
            (instructors[0], "Machine Learning", Course.COMPUTER_SCIENCE,
             4, Course.ENGLISH, True, 70),
            (instructors[1], "Web development", Course.COMPUTER_SCIENCE, 3,
             Course.FRENCH, False, 60),
            (instructors[1], "Spanish", Course.LANGUAGE, 5,
             Course.SPANISH, True, 80)
        ]
        courses = []
        for i, (instructor, title, category, duration, language, certificate, passing_grade) in enumerate(courses_metadata):
            course = Course.objects.create(
                id=i+1, instructor=instructor, title=title, category=category,
                duration=duration, language=language, certificate=certificate,
                passing_grade=passing_grade
            )
            courses.append(course)
        # Adding course 0 as a rerequisite of course 1
        courses[1].prerequisite = courses[0]
        courses[1].save()

        # Create students
        students_metadata = [
            ("Ron", [courses[0], courses[1], courses[2]]), ("Daniel", [courses[1]]), ("Jennifer", [])]
        students = []
        for i, (fname, enrolled_courses) in enumerate(students_metadata):
            student = User.objects.create(
                id=(i+1) + len(instructors), email=f"{fname}@example.com", first_name=fname, role=User.STUDENT,
                about=f"About {fname}", username=fname)
            student.enrolled_courses.set(enrolled_courses)
            students.append(student)

        # Adding passers of the courses
        courses[0].passers.set([students[1]])
        courses[1].passers.set([students[0], students[1], students[2]])

    def test_courses_count(self):
        self.assertEqual(Course.objects.count(), 3)

    def test_users_count(self):
        self.assertEqual(User.objects.count(), 5)

    def test_students_count(self):
        students = User.objects.filter(role=User.STUDENT)
        self.assertEqual(students.count(), 3)

    def test_instructors_count(self):
        students = User.objects.filter(role=User.INSTRUCTOR)
        self.assertEqual(students.count(), 2)

    def test_instructor_title(self):
        user = User.objects.get(username="Joseph")
        self.assertEqual(user.instructor_title, "Python Instructor")

    def test_about(self):
        user = User.objects.get(username="Ron")
        self.assertEqual(user.about, "About Ron")

    def test_user_enrolled_courses_count(self):
        user = User.objects.get(username="Ron")
        self.assertEqual(user.enrolled_courses.count(), 3)

    def test_user_enrolled_courses(self):
        user = User.objects.get(username="Ron")
        self.assertEqual(user.enrolled_courses.all()[0].id, 1)

    def test_course_category(self):
        course = Course.objects.get(id=2)
        self.assertEqual(course.category, Course.COMPUTER_SCIENCE)

    def test_course_language(self):
        course = Course.objects.get(id=3)
        self.assertEqual(course.language, Course.SPANISH)

    def test_course_certificate(self):
        course = Course.objects.get(id=1)
        self.assertEqual(course.certificate, True)

    def test_course_passers_count(self):
        course = Course.objects.get(id=1)
        self.assertEqual(course.passers.count(), 1)

    def test_course_passers(self):
        course = Course.objects.get(id=1)
        self.assertEqual(course.passers.all()[0].id, 4)

    def test_student_courses_passed_count(self):
        student = User.objects.get(id=4)
        self.assertEqual(student.courses_passed.count(), 2)

    def test_course_instructor(self):
        course = Course.objects.get(id=2)
        self.assertEqual(course.instructor.id, 2)

    def test_course_prerequisite_available(self):
        course = Course.objects.get(id=2)
        self.assertIsNotNone(course.prerequisite)

    def test_course_prerequisite(self):
        course = Course.objects.get(id=2)
        self.assertEqual(course.prerequisite, Course.objects.get(id=1))

    def test_course_prerequisite_not_available(self):
        course = Course.objects.get(id=1)
        self.assertIsNone(course.prerequisite)

    def test_course_1_enrolled_students_count(self):
        course = Course.objects.get(id=1)
        self.assertEqual(course.enrolled_students.count(), 1)

    def test_course_2_enrolled_students_count(self):
        course = Course.objects.get(id=2)
        self.assertEqual(course.enrolled_students.count(), 2)

    def test_instructor_courses_count(self):
        instructor = User.objects.get(id=2)
        self.assertEqual(instructor.courses_taught.count(), 2)

    def test_instructor_courses(self):
        instructor = User.objects.get(id=2)
        courses = [Course.objects.get(id=2),
                   Course.objects.get(id=3)]
        self.assertQuerysetEqual(instructor.courses_taught.all(),
                                 courses, ordered=False)

    def test_instructor_2_total_students_count(self):
        instructor = User.objects.get(id=2)
        student_count = 0
        for course in instructor.courses_taught.all():
            student_count += course.enrolled_students.count()
        self.assertEqual(student_count, 3)

    def test_instructor_1_total_students_count(self):
        instructor = User.objects.get(id=1)
        student_count = 0
        for course in instructor.courses_taught.all():
            student_count += course.enrolled_students.count()
        self.assertEqual(student_count, 1)
