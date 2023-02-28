import os
from flask import Flask, request, json,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# working on the database
# Setting the base directory where SQLAlchem should save my db file

basedir = os.path.abspath(os.path.dirname(__file__))
# In this, am telling SQLAlchemy tha in the os library, set a path, 
# the absolute path is a function that takes in the path of the working directory, where this file is.
conn = os.path.join(basedir, 'users.db')
# configuring the application/connecting to the database
app.config['SQLALCHEMY_DATABASE_URI'] =\
                                'sqlite:///'+conn

# having the db as an instance of the SQLAlchemy
db = SQLAlchemy(app)

# designing my model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(100), nullable = False, unique=True)
    lastname = db.Column(db.String(100), nullable=False,unique=True)
    contact = db.Column(db.String(100), nullable=False,unique=True)
    location = db.Column(db.String(100), nullable=True, unique=False)

    def __repr__(self):
        name = self.firstname +" " +self.lastname
        return f'user with id {self.id} is {name}'
    


    # setting the routtes for the app
    # index route
@app.route('/')
def index():
    return "Welacome to my users' table"

# Getting all users   
@app.route('/users', methods=['GET'])
def get_users():
    lsUsers=Users.query.all()

    output = []
    for user in lsUsers:
        UserDetails = {'name': user.firstname, 'lastname':user.lastname, 'contact':user.contact, 'location':user.location }
        output.append(UserDetails)
    return {'Users': output}

# Getting a specific user
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = Users.query.get_or_404(id)
    return jsonify({f"User {user.id}'s details":{'name': user.firstname, 'lastname':user.lastname, 'contact':user.contact, 'location':user.location }})

# Adding a user
@app.route('/users/add_user', methods=['POST'])
def add_user():
    user = Users(firstname=request.json['firstname'], lastname=request.json['lastname'], contact=request.json['contact'], location=request.json['location'])
    db.session.add(user)
    db.session.commit()
    return f'You successfully added user with is {user.id}'

# deleting a user
@app.route('/users/delete_user/<id>',methods=['DELETE'])
def delete_user(id):
    user = Users.query.get(id)
    # if the deleted user does not exist
    if  user is None:
        return "Error : Not found"
    db.session.delete(user)
    db.session.commit()
    return "Successfully deleted  the user"
    
# Updating a user
@app.route('/users/update/<id>', methods=[''])
def upadate(id):
    details = Users.query.patch(id)
    details.firstname = request.json['firstname']
    db.session.commit()
    return f'You successfully changed user {details.id} firstname to {details.firstname}'


