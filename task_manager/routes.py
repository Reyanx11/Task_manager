from flask import render_template,flash,redirect,url_for,request
from task_manager.forms import RegistrationForm, LoginForm,EditProfile, TaskForm
from task_manager import db,bcrypt
from task_manager.models import User, Task
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

#Logout route   
    @app.route('/logout')
    @login_required
    def logout():
        logout_user() 
        flash('You have been logged out successfully', 'info')
        return redirect(url_for('home'))
    
#edit profile
    @app.route('/edit_profile', methods=['POST','GET'])
    @login_required
    def edit_profile():
        form = EditProfile()

        if form.validate_on_submit():

            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()

            flash('your account has been updated','success')
            return  redirect(url_for('home'))
        elif request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email

        return render_template('profile.html', title = 'Edit Profile',form = form)
    
#Task route
    @app.route('/tasks', methods=['POST','GET'])
    @login_required
    def tasks():
        form = TaskForm()

        if form.validate_on_submit():
            task = Task(
                title = form.title.data,
                deadline = form.deadline.data,
                owner = current_user
            )
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('tasks'))
        
        user_tasks = Task.query.filter_by(user_id = current_user.id).order_by(Task.date_created.desc()).all()
        return render_template('tasks.html', form=form, title = 'task',tasks=user_tasks)

#updating task
    @app.route('/update_task/<int:task_id>/<string:action>', methods=['POST'])
    @login_required
    def update_task(task_id,action):
        task = Task.query.get_or_404(task_id)
        if task.owner != current_user:
            flash("You are not allowed to modify this task.", "danger")
            return redirect(url_for('tasks'))
    #actions for buttons    
        if action == 'complete':
            task.is_completed = True
        elif action == 'undo':
            task.is_completed = False
        if action == 'delete':
            db.session.delete(task)
        
        db.session.commit()
        return redirect(url_for('tasks'))