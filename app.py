# app.py

from flask import *
from werkzeug.utils import secure_filename
from config import *
from forms import *
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy.sql.expression import func

from models import db, User, Repository, Image

app = Flask(__name__, static_folder='static/', static_url_path='/', template_folder='templates')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()


# * BEFORE_REQUEST
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home', 'repository', 'image_create', 'repository_create',
    'view_repository']:
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
    # return 'Hola Mundo'
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


# * LOGOUT
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))


# * HOME
@app.route('/home')
def home():
    images = Image.query.order_by(func.random()).all()
    images_home = []

    username = session['username']
    
    for image in images:
        rep = Repository.query.filter_by(id=image.repository).first()
        user = User.query.filter_by(username=rep.username).first()

        setattr(image, 'username', user.username)

        if rep.username != username:
            # images_home.append(Image(image.repository, image.name, image.description, image.file, image.tags))
            images_home.append(image)
        else:
            continue

    title = 'imagea - Home'
    name = session['name']
    return render_template('home.html', title=title, name=name, images=images_home)


# * REPOSITORY
@app.route('/repository', methods=['GET'])
def repository():
    repositoryForm = RepositoryForm(request.form)
    username = session['username']

    reps = Repository.query.filter_by(username=username).all()
    
    num_img = []

    for rep in reps:
        num = Image.query.join(Repository).filter(rep.id == Image.repository).count()
        num_img.append(num)
        setattr(rep, 'num', num)
    
    for num in num_img:
        print(num)

    title = 'imagea - Repositories'
    name = session['name']
    lastname = session['lastname']
    username = session['username']
    return render_template('repository.html', title=title, name=name, lastname=lastname,
                           username=username, form=repositoryForm, reps=reps, num_img=num_img)


# * REPOSITORY/CREATE
@app.route('/repository/create', methods=['POST'])
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


#* REPOSITORY/<ID>
@app.route('/repository/<int:id>')
def view_repository(id):
    repositoryForm = RepositoryForm(request.form)

    images = Image.query.filter_by(repository=id).all()
    rep = Repository.query.filter_by(id=id).first()

    for image in images:
        print(image.name, image.file)
    
    username = session['username']
    reps = Repository.query.filter_by(username=username).all()
    
    title = 'imagea - View Repository'
    return render_template('view_rep.html', images=images, title=title, name=session['name'],
    lastname=session['lastname'], username=username, rep=rep, length=len(images), 
    form=repositoryForm, reps=reps)


#* IMAGE/CREATE
@app.route('/image/create', methods=['POST'])
def image_create():
    tags = request.form['tags'].split(', ')
    
    file = request.files['file']
    cwd = os.getcwd()
    file.save(os.path.join(cwd, 'static', 'img', secure_filename(file.filename)))

    abs = os.path.join(cwd, 'static', 'img', secure_filename(file.filename))
    rel = os.path.relpath(abs)
    print(rel)

    image = Image(request.form['rep'], request.form['name'], request.form['description'],
    file.filename, tags)
    
    print(image.repository)
    print(image.file)

    db.session.add(image)
    db.session.commit()

    return redirect(url_for('repository'))


# * APP.RUN()
if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()
