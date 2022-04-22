from hmac import new
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import randint


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) #Creation de la db 

@app.route("/user", methods =["POST","GET"]) #Route de l'API
def get_users():
    if request.method == "GET" :
        result = User.query.all()
        users = []
        for row in result :
            applications=[]
            for app in row.applications:
                application = {
                    "id":app.id,
                    "appname" : app.appname,
                    "username" : app.username,
                    "lastconnection" : app.lastconnection
                }
                applications.append(application)
                
            user = {
                "id": row.id,
                "firstname": row.firstname,
                "lastname" : row.lastname,
                "age": row.age,
                "email": row.email,
                "job": row.job
            }
            users.append(user)
        return jsonify(users)
    
    if request.method == "POST" :
        data = request.json
        new_user = User(
            data['Firstname'],
            data['lastname'],
            data['age'],
            data['email'],
            data['job']
        )
        db.session.add(new_user)
        db.session.commit()
        return Response(status=200)

class User(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    job = db.Column(db.String(100))
    applications = db.relationship('Application')

    def __init__(self, firstname, lastname , age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self. email =email
        self.job = job

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.Integer)
    email = db.Column(db.String(100))
    job = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, appname, username , lastconnection):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection

faker = Faker()

def populate_tables(): 
    for n in range (0,1000):
        new_user = User(faker.first_name(), faker.last_name(), faker.pyint(0,80), faker.email(), faker.job())
        apps = ['Facebook', 'Twitter', 'Instagram', 'Linkedin', 'Youtube', 'Discord', 'Skype']
        nb_app = randint(0,6) #autant qu'on le souhaite
        applications = []
        for app_n in range (0, nb_app) :
            app = Application(apps[app_n], faker.user_name(), randint(0,10))
            applications.append(app)
        new_user.applications = applications
        db.session.add(new_user)
    db.session.commit()


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    populate_tables()
    app.run(host="0.0.0.0", port=8080, debug=True)