from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
 
 
 
 
app = Flask(__name__)
app.secret_key = "Secret Key"
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' 

ENV = 'dev'

if ENV == 'prod':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:sem@localhost/flask_crud'
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://jbbzwembnirxkl:df5f15516d0631753a0dc0338b498ff0950dfb04033e44e62db87829dea7ab66@ec2-54-235-116-235.compute-1.amazonaws.com:5432/d7r1mptlbdf4ji'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

 
#Creating model table for our CRUD database
class EmployeeData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
 
 
    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone

#Creating model table for our CRUD database
class CustomerData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
 
 
    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone
 
#This is the index route where we are going to
#query on all our employee data.
@app.route('/')
def Index():
    #all_data = Data.query.all()
 
    return render_template("index.html")

@app.route('/crud')
@login_required
def crud():
    all_employees = EmployeeData.query.all()
    all_customers = CustomerData.query.all()
 
    return render_template("crud.html", employees = all_employees, customers = all_customers, name=current_user.username)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('crud'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('New user has been created!')
        return redirect(url_for('login'))
        #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('Index'))
 
#this route is for inserting data to postgres database via html forms
@app.route('/e_insert', methods = ['POST'])
def einsert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
 
        my_data = EmployeeData(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully", "category1")
 
        return redirect(url_for('crud'))

#this route is for inserting data to postgres database via html forms
@app.route('/c_insert', methods = ['POST'])
def cinsert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
 
        my_data = CustomerData(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Customer Inserted Successfully", "category2")
 
        return redirect(url_for('crud'))
 
 
#this is our update route where we are going to update our employee
@app.route('/e_update', methods = ['GET', 'POST'])
def eupdate():
 
    if request.method == 'POST':
        my_data = EmployeeData.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
 
        db.session.commit()
        flash("Employee Updated Successfully", "category1")
 
        return redirect(url_for('crud'))

#this is our update route where we are going to update our customer
@app.route('/c_update', methods = ['GET', 'POST'])
def cupdate():
 
    if request.method == 'POST':
        my_data = CustomerData.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
 
        db.session.commit()
        flash("Customer Updated Successfully", "category2")
 
        return redirect(url_for('crud'))
 
 
 
 
#This route is for deleting our employee
@app.route('/e_delete/<id>/', methods = ['GET', 'POST'])
def edelete(id):
    my_data = EmployeeData.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully", "category1")
 
    return redirect(url_for('crud'))

#This route is for deleting our customer
@app.route('/c_delete/<id>/', methods = ['GET', 'POST'])
def cdelete(id):
    my_data = CustomerData.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Customer Deleted Successfully", "category2")
 
    return redirect(url_for('crud'))
 
 
 #Driver Code
if __name__ == "__main__":
    app.run()

#use for reference https://www.youtube.com/watch?v=XTpLbBJTOM4