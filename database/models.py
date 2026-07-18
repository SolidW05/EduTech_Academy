from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    Boolean,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from datetime import date
from config.database import engine


class Base(DeclarativeBase):
    pass


# ==========================
# Categorías
# ==========================

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    courses: Mapped[list["Course"]] = relationship(back_populates="category")


# ==========================
# Cursos
# ==========================

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(1000))

    level: Mapped[str] = mapped_column(String(50))

    duration_hours: Mapped[int]

    price: Mapped[float]

    available_slots: Mapped[int]

    active: Mapped[bool] = mapped_column(default=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id")
    )

    category: Mapped["Category"] = relationship(
        back_populates="courses"
    )

    instructors: Mapped[list["Instructor"]] = relationship(
        secondary="course_instructors",
        back_populates="courses"
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course"
    )


# ==========================
# Instructores
# ==========================

class Instructor(Base):
    __tablename__ = "instructors"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True
    )

    specialty: Mapped[str] = mapped_column(String(100))

    years_experience: Mapped[int]

    courses: Mapped[list["Course"]] = relationship(
        secondary="course_instructors",
        back_populates="instructors"
    )


# ==========================
# Relación Curso-Instructor
# ==========================

class CourseInstructor(Base):
    __tablename__ = "course_instructors"

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id"),
        primary_key=True
    )

    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("instructors.id"),
        primary_key=True
    )


# ==========================
# Estudiantes
# ==========================

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True
    )

    scholarship: Mapped[bool] = mapped_column(default=False)

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="student"
    )

    certificates: Mapped[list["Certificate"]] = relationship(
        back_populates="student"
    )


# ==========================
# Inscripciones
# ==========================

class Enrollment(Base):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    course_id: Mapped[int] = mapped_column(
        ForeignKey("courses.id")
    )

    enrollment_date: Mapped[date]

    status: Mapped[str] = mapped_column(String(30))

    progress: Mapped[float]

    student: Mapped["Student"] = relationship(
        back_populates="enrollments"
    )

    course: Mapped["Course"] = relationship(
        back_populates="enrollments"
    )


# ==========================
# Certificados
# ==========================

class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id")
    )

    course_name: Mapped[str] = mapped_column(String(150))

    issue_date: Mapped[date]

    verification_code: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    student: Mapped["Student"] = relationship(
        back_populates="certificates"
    )


# ==========================
# Crear la base de datos
# ==========================

Base.metadata.create_all(engine)