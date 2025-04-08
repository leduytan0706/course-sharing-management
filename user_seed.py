from db import db, User
from app import app
from sqlalchemy.exc import SQLAlchemyError

sample_users = [{
    "name": "Trần Nhân Phát",
    "email": "tnf0706@example.com",
    "password": "123456",
    "role": "admin",
    "description": ""  
},
{
    "name": "Lê Duy Tân",
    "email": "leduytan0706@example.com",
    "password": "123456",
    "role": "teacher",
    "description": ""  
},
{
    "name": "Vũ Xuân Nin",
    "email": "vxn5048@example.com",
    "password": "123456",
    "role": "student",
    "description": ""  
}]

def add_sample_users():
    new_users = []
    for user in sample_users:
        new_user = User(
            name=user["name"],
            email=user["email"],
            password=user["password"],
            role=user["role"],
            description=user["description"]
        )
        new_users.append(new_user)

    try:
        db.session.add_all(new_users)
        db.session.commit()
    except SQLAlchemyError as e:
        print("SQLAlchemyError",e)

with app.app_context():
    add_sample_users()
