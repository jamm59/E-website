from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,TextField,SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])


class RegisterForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])

class PostForm(FlaskForm):
    body = TextField('Message', validators=[DataRequired()])

class AddForm(FlaskForm):
    image = StringField('img_url', validators=[DataRequired(),URL(message='url not valid')])
    name = StringField('Name',validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    rating = StringField('Rating', validators=[DataRequired()])
    body = CKEditorField("Message", validators=[DataRequired()])