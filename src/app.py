# app.py

from flask import *
from config import *
from forms import *
from flask_wtf.csrf import CSRFProtect

from models import db, User, Repository, Image

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


#* BEFORE_REQUEST
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home', 'repository']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['register', 'login']:
        return redirect(url_for('home'))


# * INDEX
@app.route('/')
def index():
    return redirect(url_for('register'))


# * REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm(request.form)
    print(registerForm.name.data)
    print(registerForm.lastname.data)
    print(registerForm.username.data)
    print(registerForm.password.data)

    if request.method == 'POST' and registerForm.validate():
        user = User(registerForm.name.data, registerForm.lastname.data,
                    registerForm.username.data, registerForm.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    title = 'imagea - Register'
    return render_template('register.html', title=title, form=registerForm)


# * LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm(request.form)
    print(loginForm.username.data)
    print(loginForm.password.data)

    if request.method == 'POST' and loginForm.validate():
        username = loginForm.username.data
        password = loginForm.password.data
        user = User.query.filter_by(username=username).first()

        if user is not None and user.verifyPassword(password):
            print(f'Welcome {username}')
            session['username'] = username
            session['name'] = user.name
            session['lastname'] = user.lastname
            return redirect(url_for('home'))
        else:
            print('username or password not valid')

    title = 'imagea - Login'
    return render_template('login.html', title=title, form=loginForm)


#* LOGOUT
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))


#* HOME
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        name = session['name']
        print(username)
        print(name)
    
    title = 'imagea - Home'
    name = session['name']
    return render_template('home.html', title=title, name=name)


#* REPOSITORY
@app.route('/repository', methods=['GET'])
def repository():
    repositoryForm = RepositoryForm(request.form)

    title = 'imagea - Repositories'
    name = session['name']
    lastname = session['lastname']
    username = session['username']
    return render_template('repository.html', title=title, name=name, lastname=lastname, 
    username=username, form=repositoryForm)


#* REPOSITORY/CREATE
@app.route('/repository/create', methods = ['POST'])
def repository_create():
    repositoryForm = RepositoryForm(request.form)
    print(repositoryForm.name.data)

    if repositoryForm.validate():
        username = session['username']
        rep = Repository(username, repositoryForm.name.data)

        db.session.add(rep)
        db.session.commit()
        print('Rep creado')

    return redirect(url_for('repository'))


# * APP.RUN()
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()
