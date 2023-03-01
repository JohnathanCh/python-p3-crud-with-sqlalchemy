#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())
    
    def __repr__(self):
        return f"Student {self.id}" \
            + f"{self.name}" \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    albert_einstein = Student(
        name="Albert Einstein",
        email="albert.einstein@zurich.edu",
        grade=6,
        birthday=datetime(
            year=1879,
            month=3,
            day=14
        )
    )
    
    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )
    
    johnny = Student(
        name="Johnny",
        email="Jc@sherborne.edu",
        grade=13,
        birthday=datetime(
            year=1989,
            month=10,
            day=13
        ),
    )
    
    cam = Student(
        name="Cam",
        email="ccc@stuff.edu",
        grade=9,
        birthday=datetime(
            year=1989,
            month=11,
            day=13
        ),
    )
    
    #This doesn't work
    #Gets error: "__init__() takes 1 positional argument but 5 were given"
    # alan_turing = Student(
    #     "Alan Turing",
    #     "alan.turing@sherborne.edu",
    #     11,
    #     datetime(
    #         year=1912,
    #         month=6,
    #         day=23
    #     )
    # )
    

    session.bulk_save_objects([albert_einstein, alan_turing, johnny, cam])
    session.commit()
    
    # print(f"{albert_einstein.name}'s ID is {albert_einstein.id}.")
    # print(f"{alan_turing.name}'s ID is {alan_turing.id}.")
    
    names = session.query(Student.name).all()

    print(names)
    
    students_by_name = session.query(
        Student.name).order_by(
        Student.name).all()

    print(students_by_name)
    
    students_by_grade_desc = session.query(
            Student.name, Student.grade).order_by(
            desc(Student.grade)).all()

    print(students_by_grade_desc)
    
    oldest_student = session.query(
            Student.name, Student.birthday).order_by(
            desc(Student.grade)).first()

    print(oldest_student)
    
    count_names = session.query(Student.name).count()
    
    print(count_names)
    
    letters = session.query(Student.name).filter(Student.name.startswith('A')).count()
    
    print(letters)
    
    # for student in session.query(Student):
    #     student.grade += 1

    # session.commit()

    # print([(student.name,
    #     student.grade) for student in session.query(Student)])
    
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })

    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])
    
    einstein = session.query(Student).filter(Student.name == "Albert Einstein").first()
    
    print(session.query(Student).all())
    
    session.delete(einstein)
    session.commit()
    
    print(session.query(Student).all())



