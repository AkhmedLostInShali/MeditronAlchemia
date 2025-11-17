from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = EmailField('Введите почту', id='email', validators=[DataRequired()])
    password = PasswordField('Введите пароль', id='password', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня', id='remember_checkbox')
    submit = SubmitField('Войти', id='submit')
