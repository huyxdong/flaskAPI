'''
Python Intepreter
from models import db
db.create_all() # Create a table name 'residential'

Person.add_person('Dong Xuan Huy', 28, 186744364)
Person.get_all_person()
Person.update_person_age(186744364, 19)
Person.update_person_name(186744364, 'Dong Xuan Son')

From terminal: cat site.db -> confirm database structure
'''


import json
from flask_sqlalchemy import SQLAlchemy
from settings import app


db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'residential'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    passport = db.Column(db.Integer)

    def add_person(_name, _age, _passport):
        new_person = Person(name=_name, age=_age, passport=_passport)
        db.session.add(new_person)
        db.session.commit()

    def json(self):
        return {'name': self.name, 'age': self.age, 'passport': self.passport}

    def get_all_person():
        return [Person.json(person) for person in Person.query.all()]

    def get_person(_passport):
        return Person.json(Person.query.filter_by(passport=_passport).first())

    def delete_person(_passport):
        is_success = Person.query.filter_by(passport=_passport).delete()
        db.session.commit()
        return bool(is_success)

    def update_person_age(_passport, _age):
        person_to_update = Person.query.filter_by(passport=_passport).first()
        person_to_update.age = _age
        db.session.commit()

    def update_person_name(_passport, _name):
        person_to_update = Person.query.filter_by(passport=_passport).first()
        person_to_update.name = _name
        db.session.commit()

    def replace_person(_passport, _name, _age):
        person_to_replace = Person.query.filter_by(passport=_passport).first()
        person_to_replace.name = _name
        person_to_replace.age = _age
        db.session.commit()

    def __repr__(self):
        person_object = {
            'name': self.name,
            'age': self.age,
            'passport': self.passport
        }

        return json.dumps(person_object)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return str({
            'username': self.username,
            'password': self.password
        })

    def username_password_match(_username, _password):
        user = User.query.filter_by(username=_username).filter_by(
            password=_password).first()
        return bool(user)

    def getAllUsers():
        return User.query.all()

    def createUser(_username, _password):
        new_user = User(username=_username, password=_password)
        db.session.add(new_user)
        db.session.commit()
