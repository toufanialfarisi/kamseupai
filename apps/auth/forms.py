from flask_wtf import FlaskForm
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    BooleanField,
    IntegerField,
    SelectField,
)
from apps.auth.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("remember")
    submit = SubmitField("Log in")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_email(self, field):

        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered !")

    def validate_username(self, field):

        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is registered !")
