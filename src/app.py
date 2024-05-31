from datetime import datetime
from time import sleep
from flask import Flask, flash, redirect, render_template, session, url_for, request
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy import desc
from database import Weekday, db, db_init, User, Channel, Program
from forms import *


app = Flask(__name__)

app.config['SECRET_KEY'] = 'lab6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db_init(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday',
}

@app.route('/')
def home():
    weekday = request.args.get('weekday')
    if not weekday:
        weekday = Weekday(WEEKDAYS[datetime.now().weekday()]).value
    return render_template(
        'home.html',
        channels=Channel.query.all(),
        weekday=weekday
    )

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords must match.', 'error')
            return redirect(url_for('signup'))

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists.', 'error')
            return redirect(url_for('signup'))

        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password1, method='pbkdf2:sha1'),
            is_superuser=False
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect('/')
    return render_template('signup.html', title='Sign Up')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=username).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
        else:
            login_user(user)
        return redirect('/')
    return render_template('login.html', title='Log in')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect('/')


@app.route('/admin/', methods=['GET', 'POST'])
def admin():
    # createuserform = CreateUserForm()
    updateuserform = UpdateUserForm()
    deleteuserform = DeleteUserForm()
    
    createchannelform = CreateChannelForm()
    updatechannelform = UpdateChannelForm()
    deletechannelform = DeleteChannelForm()
    
    createprogramform = CreateProgramForm()
    updateprogramform = UpdateProgramForm()
    deleteprogramform = DeleteProgramForm()
    
    if request.method == 'POST':
        if updateuserform.updateusersubmit.data and updateuserform.validate_on_submit():
            user = User.query.filter_by(id=updateuserform.id.data).first()
            if user:
                if updateuserform.name.data:
                    user.name = updateuserform.name.data
                if updateuserform.email.data:
                    user.email = updateuserform.email.data
                if updateuserform.password.data:
                    user.password = generate_password_hash(updateuserform.password.data, method='pbkdf2:sha1')
                user.is_superuser = updateuserform.is_superuser.data
            
        if deleteuserform.deleteusersubmit.data and deleteuserform.validate_on_submit():
            user = User.query.filter_by(id=updateuserform.id.data).first()
            db.session.delete(user)
        
        
        
        if createchannelform.createchannelsubmit.data and createchannelform.validate_on_submit():
            new_channel = Channel(title=createchannelform.title.data)
            db.session.add(new_channel)
            
            
        if updatechannelform.updatechannelsubmit.data and updatechannelform.validate_on_submit():
            channel = Channel.query.filter_by(id=updatechannelform.id.data).first()
            channel.title = updatechannelform.title.data
        
        if deletechannelform.deletechannelsubmit.data and deletechannelform.validate_on_submit():
            channel = Channel.query.filter_by(id=updatechannelform.id.data).first()
            db.session.delete(channel)
        
        
        
        if createprogramform.createprogramsubmit.data and createprogramform.validate_on_submit():
            new_program = Program(
                title=createprogramform.title.data,
                start_time=createprogramform.start_time.data,
                weekday=Weekday(createprogramform.weekday.data),
                channel_id=createprogramform.channel_id.data
            )
            db.session.add(new_program)
        
        if updateprogramform.updateprogramsubmit.data and updateprogramform.validate_on_submit():
            program = Program.query.filter_by(id=updateprogramform.programid.data).first()
            print(updateprogramform.programid.data)
            if program:
                if updateprogramform.title.data:
                    program.title = updateprogramform.title.data
                if updateprogramform.start_time.data:
                    program.start_time = updateprogramform.start_time.data
                if updateprogramform.weekday.data:
                    program.weekday = Weekday(updateprogramform.weekday.data)
                if updateprogramform.channel_id.data:
                    program.channel_id = updateprogramform.channel_id.data
        
        if deleteprogramform.deleteprogramsubmit.data and deleteprogramform.validate_on_submit():
            program = Program.query.filter_by(id=deleteprogramform.id.data).first()
            db.session.delete(program)
        
        
        db.session.commit()
        
    return render_template(
        'admin.html',
        title='Admin',
        users=User.query.all(),
        
        updateuserform=updateuserform,
        deleteuserform=deleteuserform,
        
        createchannelform=createchannelform,
        updatechannelform=updatechannelform,
        deletechannelform=deletechannelform,
        
        createprogramform=createprogramform,
        updateprogramform=updateprogramform,
        deleteprogramform=deleteprogramform,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8002)