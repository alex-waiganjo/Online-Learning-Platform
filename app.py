from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_login import login_required,login_user,logout_user,current_user
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# Configs before initialization
app.config['SECRET_KEY'] = 'Onlinesysmage'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Online_Learning_Platform.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize database, JWT, and migration
db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)  # Bind app and db to Migrate

# Models

class Students(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    st_fname = db.Column(db.String(80), unique=True, nullable=False)
    st_lname = db.Column(db.String(80), unique=True, nullable=False)
    st_email = db.Column(db.String(80), unique=True, nullable=False)
    st_password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.st_fname}'


class Instructors(db.Model):
    __tablename__ = 'instructors' 

    id = db.Column(db.Integer, primary_key=True)
    ins_fname = db.Column(db.String(80), unique=True, nullable=False)
    ins_lname = db.Column(db.String(80), unique=True, nullable=False)
    ins_email = db.Column(db.String(80), unique=True, nullable=False)
    ins_password = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.ins_fname}'


class Courses(db.Model):
    __tablename__ = 'courses' 

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    course_description = db.Column(db.String(80), unique=True, nullable=False)
    course_image = db.Column(db.String(80), unique=True, nullable=False)
    course_author = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.course_name}'

# Routes
# Home Page
@app.route("/", methods=['GET'])
def index_page():
    return render_template("home.html")

# Student Register Page
@app.route("/student_register", methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
       fname= request.form.get('fname')
       lname= request.form.get('lname')
       email= request.form.get('email')
       pwd= request.form.get('password')
       hashed_student_password = generate_password_hash(pwd)
       new_student = Students(st_fname=fname,st_lname=lname,st_email=email,st_password=hashed_student_password)
       db.session.add(new_student)
       db.session.commit()
    return render_template("student_register.html")

# Student Login Page
@app.route("/student_login", methods=['GET', 'POST'])
def student_login():
     if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('pwd1')  
        student = Students.query.filter_by(st_email=email).first()
     return render_template("student_login.html")

# Student Home Page
@app.route("/student_home_page", methods=['POST', 'GET'])
def student_home_page():
    return render_template("student_home_page.html")

# Instructor Register page
@app.route("/instructor_register",methods=['GET','POST'])
def instructor_register():
     if request.method == 'POST':
       ins_fname= request.form.get('fname')
       ins_lname= request.form.get('lname')
       ins_email= request.form.get('email')
       ins_pwd= request.form.get('password')
       
       hashed_instructor_password = generate_password_hash(ins_pwd)

       new_instructor = Instructors(ins_fname=ins_fname,ins_lname=ins_lname,ins_email=ins_email,ins_password=hashed_instructor_password)
       db.session.add(new_instructor)
       db.session.commit()
     return render_template("instructor_register.html")

# Instructor Login page
@app.route("/instructor_login")
def instructor_login():
    return render_template("instructor_login.html")

# Instructor Home page
@app.route("/instructor_home_page", methods=['POST', 'GET'])
def instructor_home_page():
    return render_template("instructor_home_page.html")


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
