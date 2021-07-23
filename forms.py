# forms.py

from wtforms import *
from models import User
from flask_wtf.file import *


#* REGISTERFORM
class RegisterForm(Form):
    name = StringField('Name', [validators.Required(message='Name is required')], render_kw={
        "placeholder": "Name",
        "title": "Insert your name"
        })
    
    lastname = StringField('Lastname', [validators.Required(message='Lastname is required')], 
    render_kw={ 
        "placeholder": "Lastname",
        "title": "Insert your lastname"
        })
    
    username = StringField('Username', [validators.Required(message='Username is required')], 
    render_kw={
        "placeholder": "Create a username",
        "title": "Create a username"
        })
    
    password = PasswordField('Password', [validators.Required(message='Password is required')], 
    render_kw={
        "placeholder": "Create a password",
        "title": "Create a password"
        })
    

    # VALIDATE_USERNAME()
    def validate_username(form, field): #* Reescribe la funcion generada por validators
        username = field.data

        user = User.query.filter_by(username = username).first()
        if user is not None:
             raise validators.ValidationError('El username ya se encuentra registrado')



#* LOGINFORM
class LoginForm(Form):
    username = StringField('Username', [validators.Required(message='Username is required')], 
    render_kw={
        "placeholder": "Username",
        "title": "Insert your username"
        })
    
    password = PasswordField('Password', [validators.Required(message='Password is required')], 
    render_kw={
        "placeholder": "Password",
        "title": "Insert your password"
        })


#* REPOSITORYFORM
class RepositoryForm(Form):
    name = StringField('Repository Name', [validators.Required(message='Name is required')],
    render_kw={
        "placeholder": "E.g.: Landscape, Handcraft, Cosplays",
        "title": "Insert the name of the repository"
    })


#* USERFORM
class UserForm(Form):
    name = StringField('Name', [validators.Required(message='Name is required')], render_kw={
        "placeholder": "Name",
        "title": "Edit your name"
    })

    lastname = StringField('Lastname', [validators.Required(message='Lastname is required')], render_kw={
        "placeholder": "Lastname",
        "title": "Edit your lastname"
    })

    username = StringField('Username', [validators.Required(message='Username is required')], render_kw={
        "placeholder": "Username",
        "title": "Edit your username"
    })

    password = PasswordField('Password', [validators.Required(message='Password is required')], render_kw={
        "placeholder": "Password",
        "title": "Edit your password"
    })

    # VALIDATE_USERNAME()
    def validate_username(form, field): #* Reescribe la funcion generada por validators
        username = field.data

        user = User.query.filter_by(username = username).first()
        if user is not None:
             raise validators.ValidationError('El username ya se encuentra registrado')