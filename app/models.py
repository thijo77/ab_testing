from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Testeur(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre_classe=db.Column(db.Integer, index=True)
    nombre_utilisateur=db.Column(db.Integer, index=True)
    nombre_jour=db.Column(db.Integer, index=True)
    parametre_teste=db.Column(db.String(63), index=True)

    def __repr__(self):
        return '<Testeur nbclass : {} nbuser : {}> '.format(self.id, self.nombre_classe, self.nombre_utilisateur)

class Observation(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    classe_renvoyee=db.Column(db.String(63), index=True)
    feedback=db.Column(db.Integer, index=True)
    date_creation = db.Column(db.DateTime, default= datetime.now())
    date_feedback = db.Column(db.DateTime)
    testeur_id=db.Column(db.Integer, db.ForeignKey('testeur.id'))
    
    def __repr__(self):
        return '<Observation id : {} classe_renvoyee : {} feedback : {}  date_creation = {} testeur_id : {} >'.format(self.id, self.classe_renvoyee, self.feedback, self.date_creation, self.testeur_id)

