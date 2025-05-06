from flask import Flask, render_template, request, url_for, jsonify, make_response
from datetime import date, datetime, time
from babel.dates import format_date, format_datetime, format_time
from sqlalchemy.exc import SQLAlchemyError
from flask_migrate import Migrate
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.secret_key="WEB_DEV_COURSE"

# Configuration       
cloudinary.config( 
    cloud_name = "dtlz0jfb6", 
    api_key = "364415425436136", 
    api_secret = "ukOrpbutb-rc6eIpyKcykK-J5wI", # Click 'View API Keys' above to copy your API secret
    secure=True
)

from db import db, Category, Course, Lesson, User
migrate = Migrate(app, db)
db.init_app(app)
    
with app.app_context():
    db.create_all()

@app.route("/admin", methods=["GET", "POST"])
def index():
    html_resp = render_template("admin_home.html")
    resp = make_response(html_resp)
    resp.set_cookie('user_id','2',max_age=60*60*24)
    return resp 

@app.route("/admin/courses", methods=["GET", "POST"])
def courses_page(): 
    return render_template("admin_courses.html")

@app.route("/admin/courses/<int:id>", methods=["GET"])
def detail_course_page(id):
    return render_template("courses/admin_courses_detail.html")

@app.route("/admin/courses/new", methods=["GET"])
def add_course_page():
    return render_template("courses/admin_courses_create.html")

@app.route("/admin/courses/update/<int:id>", methods=["GET"])
def update_course_page(id):
    return render_template("courses/admin_courses_update.html")

@app.route("/admin/lessons", methods=["GET"])
def lessons_page(): 
    return render_template("admin_lessons.html")

@app.route("/admin/lessons/<int:id>", methods=["GET"])
def detail_lesson_page(id): 
    return render_template("lessons/admin_lessons_detail.html")

@app.route("/admin/lessons/new", methods=["GET"])
def add_lesson_page(): 
    return render_template("lessons/admin_lessons_create.html")

@app.route("/admin/lessons/update/<int:id>", methods=["GET"])
def update_lesson_page(id): 
    return render_template("lessons/admin_lessons_update.html")

@app.route("/api/admin/courses", methods=["GET"])
def get_courses():
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        courses = []
        if user.role == "teacher":
            courses = Course.query\
                .filter(Course.teacher_id==user_id)\
                .order_by(Course.created_at.desc())\
                .all()
        else: 
            courses = Course.query\
                .order_by(Course.created_at.desc())\
                .all()
        if not courses:
            return jsonify({
                "message": "No courses found"
            }), 404

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
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        selectedCourse = Course.query.get_or_404(id)
        if not selectedCourse:
            return jsonify({
                "message": "Course not found"
            }), 404
        return jsonify({
            "course": selectedCourse.to_dict()
        }), 200
    except:
        print("Error getting lesson by id")
        return jsonify({
            "message": "There was an error getting course. Try again later."
        }), 500
    

@app.route("/api/admin/courses/new", methods=["GET", "POST"])
def add_course():
    user_id = request.cookies.get("user_id", 2) # giả sử user id 2 là teacher

    user = User.query.get_or_404(user_id)
    if not user or user.role not in ["teacher","admin"]:
        return jsonify({
            "message": "Unauthorized access"
        }), 400
    
    if request.method == "POST":
        new_course_data = {
            "name": request.form.get("name"),
            "intro": request.form.get("intro"),
            "image": request.files.get("image",None),
            "number_of_lessons": request.form.get("number_of_lessons"),
            "category": request.form.get("category"),
            "level": request.form.get("level"),
            "description": request.form.get("description")
        }
        print(new_course_data)

        category_id = ""
        category = Category.query.filter(Category.name==new_course_data["category"]).first()
        if category:
            category_dict = category.to_dict()
            category_id = category_dict['id']

        # image_url = ""
        # Logic gửi dữ liệu ảnh lên cloudinary
        image_url = ""
        if new_course_data["image"]:
            response = cloudinary.uploader.upload(new_course_data["image"])
            print(response)
            image_url = response['secure_url']

        new_course = Course(
            name=new_course_data["name"],
            intro=new_course_data["intro"],
            image_url=image_url if image_url else "",
            number_of_lessons=new_course_data["number_of_lessons"],
            category_id=category_id,
            level=new_course_data["level"],
            description=new_course_data["description"],
            teacher_id=user_id
        )

        for i in range(1, int(new_course_data["number_of_lessons"])+1):
            lesson_name = request.form.get(f'lessons[{i}][name]')
            lesson_content = request.form.get(f'lessons[{i}][content]')
            lesson_video = request.files.get(f'lessons[{i}][video]', None)
            lesson_video_url = ""

            # Thêm logic xử lý gửi video lên cloudinary sau đó nhận url về và thêm vào
            if lesson_video:
                response = cloudinary.uploader.upload(lesson_video, resource_type='video')
                lesson_video_url = response['secure_url']

            new_lesson = Lesson(
                name=lesson_name,
                content=lesson_content,
                video_url=lesson_video_url if lesson_video_url else "",
                teacher_id=user_id
            )
            new_course.lessons.append(new_lesson)

        try:
            db.session.add(new_course)
            db.session.commit()
            print("Thêm mới khóa học thành công")
            return jsonify({
                "message": "Course created successfully!",
                "course_id": new_course.id
            }), 201
        except SQLAlchemyError as e:
            print("Error adding new course:", e)
            return jsonify({
                "message": "There was an error adding your course. Try again later."
            }), 500
    return jsonify({
        "message": "Undefined route"
    }), 404

@app.route("/api/admin/courses/update/<int:id>", methods=["PUT"])
def update_course(id):
    user_id = request.cookies.get("user_id", 2) # giả sử user id 2 là teacher

    user = User.query.get_or_404(user_id)
    if not user or user.role not in ["teacher","admin"]:
        return jsonify({
            "message": "Unauthorized access"
        }), 400
    
    selected_lesson = Lesson.query.get_or_404(id)
    if not selected_lesson:
        return jsonify({
            "message": "Lesson not found"
        }), 404

    updated_course_data = {
        "name": request.form.get("name"),
        "intro": request.form.get("intro"),
        "image": request.files.get("image",""),
        "number_of_lessons": request.form.get("number_of_lessons"),
        "category": request.form.get("category"),
        "level": request.form.get("level"),
        "description": request.form.get("description")
    }
    print(updated_course_data)

    category_id = ""
    category = Category.query.filter(Category.name==updated_course_data["category"]).first()
    if category:
        category_dict = category.to_dict()
        category_id = category_dict['id']

    # image_url = ""
    # Logic gửi dữ liệu ảnh lên cloudinary
    image_url = selected_lesson.image_url
    if updated_course_data["image"]:
        response = cloudinary.uploader.upload(updated_course_data["image"])
        image_url = response['secure_url']


    # new_course = Course(
    #     name=updated_course_data["name"],
    #     intro=updated_course_data["intro"],
    #     image_url=image_url if image_url else "",
    #     number_of_lessons=updated_course_data["number_of_lessons"],
    #     category_id=updated_course_data["category"],
    #     level=updated_course_data["level"],
    #     description=updated_course_data["description"],
    #     teacher_id=user_id
    # )

    try:
        # db.session.add(new_course)
        db.session.query(Course).filter(id==id).update({
            "name": updated_course_data["name"],
            "intro": updated_course_data["intro"],
            "image_url": image_url,
            "number_of_lessons": updated_course_data["number_of_lessons"],
            "category_id": category_id,
            "level": updated_course_data["level"],
            "description": updated_course_data["description"]
        })
        db.session.commit()
        print("Cập nhật khóa học thành công")
        return jsonify({
            "message": "Course created successfully!",
            "course_id": id
        }), 200
    except SQLAlchemyError as e:
        print("Error updating course:", e)
        return jsonify({
            "message": "There was an error updating your course. Try again later."
        }), 500
    
@app.route("/api/admin/courses/delete/<int:id>", methods=['DELETE'])
def delete_course(id):
    user_id = request.cookies.get("user_id", 2)
    user = User.query.get_or_404(user_id)
    if not user or user.role not in ["teacher","admin"]:
        return jsonify({
            "message": "Unauthorized access"
        }), 400
    
    try:
        response = Lesson.query.filter(Lesson.course_id==id).delete()

        response = Course.query.filter(Course.id==id).delete()
        db.session.commit()
        return jsonify({
            "message": "Course deleted successfully!"
        }), 200
    except SQLAlchemyError as e:
        print("Error updating course:", e)
        return jsonify({
            "message": "There was an error updating your course. Try again later."
        }), 500

@app.route("/api/admin/lessons", methods=["GET", "POST"])
def get_lessons(): 
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(int(user_id))
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        
        lessons = []
        if user.role == "teacher":
            lessons = Lesson.query\
                .filter(Lesson.teacher_id==user_id)\
                .order_by(Lesson.created_at.desc())\
                .all()
        else:
            lessons = Lesson.query\
                .order_by(Lesson.created_at.desc())\
                .all()
        print(lessons)

        if not lessons:
            return jsonify({
                "message": "No courses found"
            }), 404

        lessons_dict = [lesson.to_dict() for lesson in lessons]

        return jsonify({
            "lessons": lessons_dict
        }), 200

    except SQLAlchemyError as e:
        print("Error getting lessons:", e)
        return jsonify({
            "message": "There was an error getting courses. Try again later."
        }), 500
    
@app.route("/api/admin/lessons/<int:id>", methods=["GET"])
def get_lesson_by_id(id):
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        selected_lesson = Lesson.query.get_or_404(id)
        if not selected_lesson:
            return jsonify({
                "message": "Lesson not found"
            }), 404
        
        selected_course = Course.query.get_or_404(selected_lesson.course_id)
        if not selected_course:
            return jsonify({
                "message": "Course not found"
            }), 404
        
        return jsonify({
            "lesson": {
                **selected_lesson.to_dict(),
                "courseName": selected_course.name 
            }
        }), 200
    except:
        print("Error getting lesson")
        return jsonify({
            "message": "There was an error getting lesson. Try again later."
        }), 500

@app.route("/api/admin/lessons/new", methods=["POST"])
def add_lesson():
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        course_id = request.form.get("courseId", "")
        selected_course = Course.query.get_or_404(course_id)
        if not selected_course:
            return jsonify({
                "message": "Course not found."
            })
        
        lesson_video = request.files.get("lessonVideo", None)
        lesson_video_url = ""
        if lesson_video:
            response = cloudinary.uploader.upload(lesson_video, resource_type='video')
            lesson_video_url = response['secure_url']

        new_lesson = Lesson(
            name=request.form.get("lessonName"),
            content=request.form.get("lessonContent"),
            video_url=lesson_video_url,
            teacher_id=user_id,
            course_id=selected_course.id
        )

        db.session.add(new_lesson)
        db.session.commit()
        print("Thêm mới bài học thành công!")
        return jsonify({
            "message": "Lesson created successfully!",
            "lesson_id": new_lesson.id
        }), 201

    except SQLAlchemyError as e:
        print("Error adding lesson:", e)
        return jsonify({
            "message": "There was an error adding lesson. Try again later."
        }), 500

@app.route("/api/admin/lessons/update/<int:id>", methods=["PUT"])
def update_lesson(id):
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        
        selected_lesson = Lesson.query.get_or_404(id)
        if not selected_lesson:
            return jsonify({
                "message": "Lesson not found."
            }), 404
        

        course_id = request.form.get("courseId", "")
        selected_course = Course.query.get_or_404(course_id)
        if not selected_course:
            return jsonify({
                "message": "Course not found."
            })
        
        lesson_video = request.files.get("lessonVideo", None)
        lesson_video_url = selected_lesson.video_url
        if lesson_video:
            response = cloudinary.uploader.upload(lesson_video, resource_type='video')
            lesson_video_url = response['secure_url']
    
        existing_video_url = selected_lesson.to_dict().video_url
        if len(existing_video_url) > 0:
            response = cloudinary.uploader.destroy(existing_video_url, resource_type='video')

        selected_lesson.name = request.form.get("lessonName")
        selected_lesson.content = request.form.get("lessonContent")
        selected_lesson.video_url = lesson_video_url
        selected_lesson.teacher_id = user_id
        selected_lesson.course_id = selected_course.id

        db.session.commit()
        print("Cập nhật bài học thành công!")
        return jsonify({
            "message": "Lesson updated successfully!",
            "lesson_id": selected_lesson.id
        }), 200

    except SQLAlchemyError as e:
        print("Error updating lesson:", e)
        return jsonify({
            "message": "There was an error updating lesson. Try again later."
        }), 500

@app.route("/api/admin/lessons/delete/<int:id>", methods=["DELETE"])
def delete_lesson(id):
    user_id = request.cookies.get("user_id", 2)
    try:
        user = User.query.get_or_404(user_id)
        if not user or user.role not in ["teacher","admin"]:
            return jsonify({
                "message": "Unauthorized access"
            }), 400
        
        selected_lesson = Lesson.query.get_or_404(id)
        if not selected_lesson:
            return jsonify({
                "message": "Lesson not found."
            }), 404
        
        response = Lesson.query.filter(Lesson.id==id).delete()
        db.session.commit()
        return jsonify({
            "message": "Lesson delete successfully!"
        }), 200
        
    except SQLAlchemyError as e:
        print("Error deleting lesson:", e)
        return jsonify({
            "message": "There was an error deleting lesson. Try again later."
        }), 500

@app.route("/api/admin/teachers", methods=["GET"])
def get_teachers():
    try:
        teachers = User.query.filter(User.role=="teacher").all()
        if not teachers:
            return jsonify({
                "message": "No courses found"
            }), 404

        teachers_dict = [teacher.to_dict() for teacher in teachers]

        return jsonify({
            "teachers": teachers_dict
        }), 200

    except SQLAlchemyError as e:
        print("Error getting courses:", e)
        return jsonify({
            "message": "There was an error getting courses. Try again later."
        }), 500

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

@app.route('/api/image-placeholder')
def get_image_url():
    url = url_for('static', filename='images/course_placeholder.svg')
    return jsonify({'image_url': url}), 200


if __name__ == '__main__':
    app.run(debug=True)

