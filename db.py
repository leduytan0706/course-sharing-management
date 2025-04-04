from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    avatar = db.Column(db.Text, default="https://res.cloudinary.com/dtlz0jfb6/image/upload/v1743412801/xzcj4oza387tbujbevnn.jpg")

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    image_url = db.Column(db.Text, default="")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    intro = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    number_of_students = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    number_of_lessons = db.Column(db.Integer, default=0)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))
    image_url = db.Column(db.Text, default="")
    teacher = db.relationship("Teacher", backref="courses")

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    content = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.Text, nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))