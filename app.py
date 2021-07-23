# app.py

from flask import *
from werkzeug.utils import secure_filename
from config import *
from forms import *
from flask_wtf.csrf import CSRFProtect
import os
from sqlalchemy.sql.expression import func

from models import db, User, Repository, Image

app = Flask(__name__, static_folder='static/',
            static_url_path='/', template_folder='templates')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)


# * BEFORE_REQUEST
@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['home', 'repository', 'image_create', 'repository_create',
                                                          'view_repository', 'image_search', 'user_edit_view']:
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
    username = session['username']

    images = db.session.query(Image.name, Image.file, User.username).filter(
    Image.repository == Repository.id).filter(Repository.username == User.username).filter(
    User.username != username).order_by(func.random()).all()

    title = 'imagea - Home'
    name = session['name']
    return render_template('home.html', title=title, name=name, images=images)


# * REPOSITORY
@app.route('/repository', methods=['GET'])
def repository():
    repositoryForm = RepositoryForm(request.form)
    username = session['username']

    reps = Repository.query.filter_by(username=username).all()

    num_img = []

    for rep in reps:
        num = Image.query.join(Repository).filter(
            rep.id == Image.repository).count()
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


# * REPOSITORY/<ID>
@app.route('/repository/<int:id>')
def view_repository(id):
    repositoryForm = RepositoryForm(request.form)

    images = Image.query.filter_by(repository=id).all()
    rep = Repository.query.filter_by(id=id).first()

    username = session['username']
    reps = Repository.query.filter_by(username=username).all()

    title = 'imagea - View Repository'
    return render_template('view_rep.html', images=images, title=title, name=session['name'],
                           lastname=session['lastname'], username=username, length=len(images),
                           form=repositoryForm, reps=reps, rep=rep)


# * IMAGE/CREATE
@app.route('/image/create', methods=['POST'])
def image_create():
    tags = request.form['tags'].split(', ')

    file = request.files['file']
    cwd = os.getcwd()
    file.save(os.path.join(cwd, 'static', 'img',
              secure_filename(file.filename)))

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


#* IMAGE/SEARCH
@app.route('/image/search', methods=['POST'])
def image_search():
    search = request.form['search']

    images = db.session.query(Image.name, Image.file, User.username).filter(Image.tags.any(search)).filter(
    Image.repository == Repository.id).filter(Repository.username==User.username).all()

    title = 'imagea - Search'
    name = session['name']
    return render_template('search.html', images=images, name=name, title=title)


#* USER/EDIT - GET
@app.route('/user/edit', methods=['GET'])
def user_edit_view():
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    userForm = UserForm(request.form)
    userForm.name.data = user.name
    userForm.lastname.data = user.lastname
    userForm.username.data = user.username
    userForm.password.data = user.password

    title = 'imagea - Edit User'
    name = session['name']
    print(name)
    return render_template('user_edit.html', user=user, form=userForm, name=name, title=title)


#* USER/EDIT - PUT
@app.route('/user/edit', methods=['PUT'])
def user_edit():
    username = session['username']

    user = User.query.get(username)

    name = request.form['name']
    lastname = request.form['lastname']
    username_new = request.form['username']
    # password = request.form['password']

    user.name = name
    user.lastname = lastname
    user.username = username_new

    db.session.commit()
    session['username'] = username_new

    print(name, lastname, username_new)

    return { 'status': 200, 'user': {
        'name': name,
        'lastname': lastname,
        'username': username_new,
    }}


#* USER/DELETE
@csrf.exempt
@app.route('/user/delete', methods=['DELETE'])
def user_delete():
    username = session['username']

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()

    return { 'status': 200, 'user': {
        'name': user.name,
        'lastname': user.lastname,
        'username': user.username,
        'password': user.password
    }}


#* PRUEBA DELETE
# @csrf.exempt
# @app.route('/user/edit', methods=['DELETE'])
# def prueba():
#     return { 'message': 'DELETE' }


# * APP.RUN()
db.init_app(app)
if __name__ == '__main__':
    csrf.init_app(app)
    # db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()
