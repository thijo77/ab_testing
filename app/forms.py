from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ExperienceForm(FlaskForm):
    nombre_classe=IntegerField('Nombre de classe', validators=[DataRequired()])
    nombre_utilisateur=IntegerField('Nombre d utilisateur', validators=[DataRequired()])
    duree_test=IntegerField('Duree du test (en jour)', validators=[DataRequired()])
    parametre_teste=StringField('Parametre', validators=[DataRequired()])
    soumettre=SubmitField('Soumettre')

