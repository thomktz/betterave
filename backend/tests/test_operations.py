import unittest
from main import app, db
from app.database import operations
from app.models.class_ import Class
from app.models.student import Student

class TestOperations(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_add_and_get_student(self):
        student_id = operations.add_student(
            "Alice", "Bob", "", "1A", []
        )
        student = operations.get_student_by_id(student_id)
        self.assertEqual(student.name, "Alice")

    def test_add_and_get_class(self):
        class_id = operations.add_class(
            1, "Econométrie", 4, "Mr. Econométrie"
        )
        cls = db.session.get(Class, class_id)
        self.assertEqual(cls.name, "Econométrie")

    def test_get_student_by_email(self):
        operations.add_student(
            "Alice", "Bob", "", "2A", []
        )
        student = operations.get_student_by_email("alice.bob@ensae.fr")
        self.assertEqual(student.name, "Alice")

    def test_authenticate_student(self):
        operations.add_student(
            "Alice", "Bob", "", "3A", []
        )
        auth = operations.authenticate_student("alice.bob@ensae.fr", "abob")
        self.assertTrue(auth)

    def test_get_all_students(self):
        operations.add_student("A", "B", "", "1A", [])
        operations.add_student("C", "D", "", "2A", [])
        students = operations.get_all_students()
        self.assertEqual(len(students), 2)

    def test_get_all_classes(self):
        operations.add_class("1", "Econométrie", 4, "Mr. Econométrie")
        operations.add_class("2", "Statistiques", 3, "Mme. Statistiques")
        classes = operations.get_all_classes()
        self.assertEqual(len(classes), 2)

    def test_get_students_by_class_id(self):
        class_id = operations.add_class("3", "Microéconomie", 4.0, "Prof. Microéconomie")
        student1_id = operations.add_student("E", "F", "", "3A", [class_id])
        student2_id = operations.add_student("G", "H", "", "2A", [class_id])
        students = operations.get_students_by_class_id(class_id)
        self.assertEqual(len(students), 2)

if __name__ == '__main__':
    unittest.main()
