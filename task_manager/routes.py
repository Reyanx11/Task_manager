from flask import render_template,flash,redirect,url_for
from task_manager.forms import RegistrationForm, LoginForm
from task_manager import db,bcrypt
from task_manager.models import User
from flask_login import login_user,logout_user,current_user,login_required



def register_routes(app):
    @app.route('/')
    def home():
        return render_template('home.html')

#login route
    @app.route('/login', methods=['POST','GET'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first() #filters username by using email
            #checking email and pass
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)   
                flash(f'Login Successful', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful, check your username and password', 'danger')
        return render_template('login.html', title = 'Login', form=form)

#register route
    @app.route('/register', methods=['POST','GET'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username = form.username.data, email = form.email.data, password = hashed_password)
            db.session.add(user)
            db.session.commit()
            flash (f'Account created for {form.username.data} now you can login', 'success')
            return redirect(url_for('login'))  #redirects to login page so user can log in after they register themselves
        return render_template('register.html',title = 'Register', form=form)
