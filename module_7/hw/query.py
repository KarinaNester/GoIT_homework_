from sqlalchemy import func, desc, select, and_, distinct

from module_7.myconf.models import Grade, Teacher, Student, Group, Subject
from module_7.myconf.db import session


def select_01():
    result = (
        session.query(
            Student.id,
            Student.fullname,
            func.round(func.avg(Grade.grade), 2).label('average_grade')).
            select_from(Student).
            join(Grade).group_by(Student.id).
            order_by(desc('average_grade')).limit(5).all())
    return result

def select_02():
    result = session.query(Student.id, Student.fullname, func.round(func.avg(Grade.grade), 2).label('average_grade')) \
        .select_from(Grade).join(Student).filter(Grade.subjects_id == 1).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    return result

def select_03():
    result = session.query(Student.group_id, func.avg(Grade.grade).label('average_grade')) \
        .join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subjects_id == Subject.id) \
        .filter(Subject.id == 1).group_by(Student.group_id).all()
    return result
def select_04():
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result

def select_05():
    result = (session.query(Subject.name).join(Subject.teacher).filter(Teacher.id == 1).all())
    return result
def select_06():
    students_list = session.query(Student).filter_by(group_id=1).all()
    student_names = [student.fullname for student in students_list]
    return student_names

def select_07():
    result = session.query(Grade).join(Student).join(Subject).filter(Student.group_id == 1, Subject.id == 1).all()
    # grade_ids = [grade.id for grade in grades_list]
    return result

def select_08():
    result = session.query(func.avg(Grade.grade)).join(Subject).filter(Subject.teacher_id == 1).scalar()
    return result
def select_09():
    result = session.query(Subject.name).join(Grade, Subject.id == Grade.subjects_id).filter(Grade.student_id == 1).distinct().all()

    return result
def select_10():
    result = session.query(Subject.name).join(Teacher, Teacher.id == Subject.teacher_id).filter(Teacher.id == 1).all()
    return result


if __name__ == '__main__':
    print(select_01())
    print(select_02())
    print(select_03())
    print(select_04())
    print(select_05())
    print(select_06())
    print(select_07())
    print(select_08())
    print(select_09())
    print(select_10())
