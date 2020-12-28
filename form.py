from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    title = StringField('Add Title:', validators=[InputRequired()])
    content = StringField('Add Content:', validators=[InputRequired()])
