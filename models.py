# user.py

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

#* USER
class User(db.Model):
    __tablename__ = 'usuario'

    name = db.Column(db.String(10))
    lastname = db.Column(db.String(15))
    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.String(200))
    repository = db.relationship('Repository', back_populates='usuario', cascade='all, delete')

    # CONSTRUCTOR
    def __init__(self, name, lastname, username, password):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.password = self.__createPassword(password)
    

    # CREATEPASSWORD
    def __createPassword(self, password):
        return bcrypt.generate_password_hash(password).decode('utf-8')
    

    # VERIFYPASSWORD
    def verifyPassword(self, password):
        return bcrypt.check_password_hash(self.password, password)


#* REPOSITORY
class Repository(db.Model):
    __tablename__ = 'repositorio'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), db.ForeignKey('usuario.username', ondelete='CASCADE', onupdate='CASCADE'))
    usuario = db.relationship('User', back_populates='repository')
    name = db.Column(db.String(20))
    image = db.relationship('Image', back_populates='rep', cascade='all, delete')

    # CONSTRUCTOR
    def __init__(self, username, name):
        self.username = username
        self.name = name


#* IMAGE
class Image(db.Model):
    __tablename__ = 'imagen'

    id = db.Column(db.Integer, primary_key=True)
    repository = db.Column(db.Integer, db.ForeignKey('repositorio.id', ondelete='CASCADE', onupdate='CASCADE'))
    rep = db.relationship('Repository', back_populates='image')
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    file = db.Column(db.Text())
    tags = db.Column(db.ARRAY(db.String(20)))

    # CONSTRUCTOR
    def __init__(self, repository, name, description, file, tags):
        self.repository = repository
        self.name = name
        self.description = description
        self.file = file
        self.tags = tags
