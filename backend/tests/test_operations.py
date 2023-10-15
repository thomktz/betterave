import unittest
from main import app
from extensions import db
from backend.app.operations import user_operations
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.class_ import Class


class TestOperations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_add_and_get_student(self):
        student_id = user_operations.add_student(
            "Alice", "Bob", "", "1A", []
        )
        student = user_operations.get_student_by_id(student_id)
        self.assertEqual(student.name, "Alice")

    def test_add_and_get_class(self):
        class_id = user_operations.add_class(
            1, "Econométrie", 4, "Mr. Econométrie"
        )
        cls = db.session.get(Class, class_id)
        self.assertEqual(cls.name, "Econométrie")

    def test_get_student_by_email(self):
        user_operations.add_student(
            "Alice", "Bob", "", "2A", []
        )
        student = user_operations.get_student_by_email("alice.bob@ensae.fr")
        self.assertEqual(student.name, "Alice")

    def test_authenticate_student(self):
        user_operations.add_student(
            "Alice", "Bob", "", "3A", []
        )
        auth = user_operations.authenticate_student("alice.bob@ensae.fr", "abob")
        self.assertTrue(auth)

    def test_get_all_students(self):
        user_operations.add_student("A", "B", "", "1A", [])
        user_operations.add_student("C", "D", "", "2A", [])
        students = user_operations.get_all_students()
        self.assertEqual(len(students), 2)

    def test_get_all_classes(self):
        user_operations.add_class("1", "Econométrie", 4, "Mr. Econométrie")
        user_operations.add_class("2", "Statistiques", 3, "Mme. Statistiques")
        classes = user_operations.get_all_classes()
        self.assertEqual(len(classes), 2)

    def test_get_students_by_class_id(self):
        class_id = user_operations.add_class("3", "Microéconomie", 4.0, "Prof. Microéconomie")
        student1_id = user_operations.add_student("E", "F", "", "3A", [class_id])
        student2_id = user_operations.add_student("G", "H", "", "2A", [class_id])
        students = user_operations.get_students_by_class_id(class_id)
        self.assertEqual(len(students), 2)
        
    def test_add_and_get_lesson(self):
        class_id = user_operations.add_class("1", "Econométrie", 4, "Mr. Econométrie")
        lesson_id = user_operations.add_lesson(class_id, "2023-10-10", "08:00:00", "10:00:00")
        lesson = user_operations.get_lesson_by_id(lesson_id)
        self.assertEqual(str(lesson.date), "2023-10-10")
        self.assertEqual(str(lesson.start_time), "08:00:00")

    def test_get_all_lessons(self):
        class_id = user_operations.add_class("2", "Statistiques", 3, "Mme. Statistiques")
        user_operations.add_lesson(class_id, "2023-10-11", "08:00:00", "10:00:00")
        user_operations.add_lesson(class_id, "2023-10-12", "09:00:00", "11:00:00")
        lessons = user_operations.get_all_lessons()
        self.assertEqual(len(lessons), 2)

    def test_get_lessons_by_class_id(self):
        class_id = user_operations.add_class("3", "Microéconomie", 4.0, "Prof. Microéconomie")
        user_operations.add_lesson(class_id, "2023-10-13", "10:00:00", "12:00:00")
        lessons = user_operations.get_lessons_by_class_id(class_id)
        self.assertEqual(len(lessons), 1)

    def test_get_lessons_by_student(self):
        class_id = user_operations.add_class("4", "Macroéconomie", 4.0, "Prof. Macroéconomie")
        student_id = user_operations.add_student("I", "J", "", "4A", [class_id])
        user_operations.add_lesson(class_id, "2023-10-14", "11:00:00", "13:00:00")
        lessons = user_operations.get_lessons_by_student(student_id)
        self.assertEqual(len(lessons), 1)

    def test_order_lessons_by_date_and_time(self):
        class_id = user_operations.add_class("5", "Finance", 5.0, "Prof. Finance")
        lesson1_id = user_operations.add_lesson(class_id, "2023-10-14", "14:00:00", "16:00:00")
        lesson2_id = user_operations.add_lesson(class_id, "2023-10-14", "10:00:00", "12:00:00")
        lessons = [user_operations.get_lesson_by_id(lesson1_id), user_operations.get_lesson_by_id(lesson2_id)]
        sorted_lessons = sorted(lessons)
        self.assertEqual(str(sorted_lessons[0].start_time), "10:00:00")
        self.assertEqual(str(sorted_lessons[1].start_time), "14:00:00")

if __name__ == "__main__":
    unittest.main()
