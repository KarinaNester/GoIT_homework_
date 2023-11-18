from faker import Faker
import random
from sqlalchemy.exc import SQLAlchemyError
from module_7.myconf.db import session
from module_7.myconf.models import Teacher, Student, Subject, Grade, Group

fake = Faker('uk-UA')

try:
    teachers = []
    for _ in range(3):
        teacher = Teacher(fullname=fake.name())
        teachers.append(teacher)

    session.add_all(teachers)
    session.commit()

    groups = []
    for _ in range(3):
        group = Group(name=fake.word())
        groups.append(group)

    session.add_all(groups)
    session.commit()

    # Отримання списку вчителів та груп
    teachers = session.query(Teacher).all()
    groups = session.query(Group).all()

    subjects = []
    for _ in range(5, 9):
        teacher = random.choice(teachers)
        subject = Subject(name=fake.word(), teacher=teacher)
        subjects.append(subject)

    session.add_all(subjects)
    session.commit()

    # Заповнення таблиці студентів та пов'язання з групами
    students = []
    for _ in range(30, 50):
        student = Student(fullname=fake.name())
        group = random.choice(groups)
        student.group = group
        students.append(student)

    session.add_all(students)
    session.commit()

    # Отримання списку предметів
    subjects = session.query(Subject).all()

    # Заповнення таблиці оцінок для студентів у всіх предметах
    for student in session.query(Student).all():
        subjects_for_student = random.sample(subjects, random.randint(1, len(subjects)))
        for subject in subjects_for_student:
            grade = random.randint(60, 100)
            date = fake.date_between(start_date='-1y', end_date='today')
            new_grade = Grade(grade=grade, grade_date=date, student_id=student.id, subjects_id=subject.id)
            session.add(new_grade)
    session.commit()

except SQLAlchemyError as e:
    session.rollback()
    print(f"SQLAlchemyError occurred: {e}")
finally:
    session.close()


