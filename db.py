from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    avatar = db.Column(db.Text, default="https://res.cloudinary.com/dtlz0jfb6/image/upload/v1743412801/xzcj4oza387tbujbevnn.jpg")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'description': self.description,
            'created_at': self.created_at,
            'avatar': self.avatar
        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    intro = db.Column(db.Text, nullable=False)
    level = db.Column(db.String(20))
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    number_of_students = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    number_of_lessons = db.Column(db.Integer, default=0)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    image_url = db.Column(db.Text, default="")

    lessons = db.relationship('Lesson', backref='course', cascade="all, delete-orphan")
    category = db.relationship('Category', backref='courses')
    teacher = db.relationship('User',backref='courses')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'intro': self.intro,
            'level': self.level,
            'description': self.description,
            'category': self.category.to_dict() if self.category else None,
            'number_of_students': self.number_of_students,
            'created_at': self.created_at,
            'number_of_lessons': self.number_of_lessons,
            'teacher': self.teacher.to_dict() if self.teacher else None,
            'image_url': self.image_url,
            'lessons': [lesson.to_dict() for lesson in self.lessons]
        }

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    content = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'course_id': self.course_id,
            'content': self.content,
            'video_url': self.video_url
        }

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"))