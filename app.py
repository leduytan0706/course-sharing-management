from flask import Flask, render_template, request, url_for, jsonify
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.secret_key="WEB_DEV_COURSE"

from db import db, Category, Course, Lesson, User
migrate = Migrate(app, db)
db.init_app(app)
    
with app.app_context():
    db.create_all()

@app.route("/admin", methods=["GET", "POST"])
def index():
    
    return render_template("admin_home.html")

@app.route("/admin/courses", methods=["GET", "POST"])
def courses_page(): 
    return render_template("admin_courses.html")

@app.route("/admin/courses/new", methods=["GET"])
def add_course_page():
    return render_template("courses/admin_courses_create.html")

@app.route("/admin/courses/update/<int:id>", methods=["GET"])
def update_course_form():
    if request.method == "POST":
        pass

    return render_template("courses/admin_courses_update.html")

@app.route("/api/admin/courses", methods=["GET"])
def get_courses():
    try:
        courses = Course.query.all()
        # if not courses:
        #     return jsonify({
        #         "message": "No courses found"
        #     }), 404

        courses_dict = [course.to_dict() for course in courses]

        return jsonify({
            "courses": courses_dict
        }), 200

    except SQLAlchemyError as e:
        print("Error getting courses:", e)
        return jsonify({
            "message": "There was an error getting courses. Try again later."
        }), 500
    
@app.route("/api/admin/courses/<int:id>", methods=["GET"])
def get_course_by_id(id):
    selectedCourse = None
    try:
        selectedCourse = Course.query.get_or_404(id)
        if not selectedCourse:
            return jsonify({
                "message": "Course not found"
            }), 404
        return jsonify({
            "course": selectedCourse.to_dict()
        }), 200
    except:
        print("Error getting courses")
        return jsonify({
            "message": "There was an error getting courses. Try again later."
        }), 500
    

@app.route("/api/admin/courses/new", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        new_course_data = {
            "name": request.form.get("name"),
            "intro": request.form.get("intro"),
            "image": request.files.get("image"),
            "number_of_lessons": request.form.get("number_of_lessons"),
            "category": request.form.get("category"),
            "level": request.form.get("level"),
            "description": request.form.get("description")
        }

        image_url = ""
        # Logic gửi dữ liệu ảnh lên cloudinary
        # image_url = cloudinary.uploader.upload(new_course["image"])

        # Lấy id user từ cookie
        # user_id = request.get_cookie('user', "")

        new_course = Course(
            name=new_course_data["name"],
            intro=new_course_data["intro"],
            image_url=image_url if image_url else None,
            number_of_lessons=new_course_data["number_of_lessons"],
            category_id=new_course_data["category"],
            level=new_course_data["level"],
            description=new_course_data["description"]
        )

        for i in range(1, int(new_course_data["number_of_lessons"])+1):
            lesson_name = request.form.get(f'lessons[{i}][name]')
            lesson_content = request.form.get(f'lessons[{i}][content]')
            lesson_video = request.files.get(f'lessons[{i}][video]')
            lesson_video_url = ""

            # Thêm logic xử lý gửi video lên cloudinary sau đó nhận url về và thêm vào
            # lesson_video_url = cloudinary.uploader.upload(lesson_video)

            new_lesson = Lesson(
                name=lesson_name,
                content=lesson_content,
                video_url=lesson_video_url if lesson_video_url else None
            )
            new_course.lessons.append(new_lesson)

        try:
            db.session.add(new_course)
            db.session.commit()
            print("Thêm mới khóa học thành công")
            return jsonify({
                "message": "Course created successfully!",
                "course_id": new_course.id
            }), 200
        except SQLAlchemyError as e:
            print("Error adding new course:", e)
            return jsonify({
                "message": "There was an error adding your course. Try again later."
            }), 500
    return jsonify({
        "message": "Page not found"
    }), 404

@app.route("/api/category", methods=["GET", "POST"])
def get_categories():
    categories = []

    try:
        # db.session.add(new_category)
        # db.session.commit()
        categories = Category.query.all()
        if categories == None or len(categories) == 0:
            print("Chưa thêm category")
    except:
        print("Error getting category")
    categories_dict = [{"id": category.id, "name": category.name} for category in categories]

    return jsonify({
        "categories": categories_dict
    })


if __name__ == '__main__':
    app.run(debug=True)

