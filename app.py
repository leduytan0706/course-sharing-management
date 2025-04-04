from flask import Flask, render_template, request, url_for, jsonify

from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///app.db"
app.secret_key="WEB_DEV_COURSE"

from db import db, Category
db.init_app(app)
    
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    
    return render_template("index.html")

@app.route("/category", methods=["GET", "POST"])
def category():
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

