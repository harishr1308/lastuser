# -*- coding: utf-8 -*-
import flaskext.wtf as wtf
from lastuserapp.models import User, UserEmail, getuser
from lastuserapp.utils import valid_username

class LoginForm(wtf.Form):
    username = wtf.TextField('Username or Email', validators=[wtf.Required()])
    password = wtf.PasswordField('Password', validators=[wtf.Required()])
    remember = wtf.BooleanField('Remember me')

    def validate_username(self, field):
        existing = getuser(field.data)
        if existing is None:
            raise wtf.ValidationError, "User does not exist"

    def validate_password(self, field):
        user = getuser(self.username.data)
        if user is None or not user.check_password(field.data):
            raise wtf.ValidationError, "Incorrect password"
        self.user = user


class OpenIdForm(wtf.Form):
    openid = wtf.html5.URLField('Login with OpenID', validators=[wtf.Required()],
        description="Don't forget the http:// or https:// prefix")


class RegisterForm(wtf.Form):
    fullname = wtf.TextField('Full name', validators=[wtf.Required()])
    email = wtf.html5.EmailField('Email address', validators=[wtf.Required(), wtf.Email()])
    username = wtf.TextField('Username (optional)', validators=[wtf.Optional()])
    password = wtf.PasswordField('Password', validators=[wtf.Required()])
    confirm_password = wtf.PasswordField('Confirm password',
                          validators=[wtf.Required(), wtf.EqualTo('password')])
    recaptcha = wtf.RecaptchaField('Are you human?',
        description="Type both words into the text box")

    def validate_username(self, field):
        if not valid_username(field.data):
            return wtf.ValidationError, "Invalid characters in username"
        existing = User.query.filter_by(username=field.data).first()
        if existing is not None:
            raise wtf.ValidationError, "That username is taken"

    def validate_email(self, field):
        existing = UserEmail.query.filter_by(email=field.data).first()
        if existing is not None:
            raise wtf.ValidationError, Markup(
                'This email address is already registered. Do you want to <a href="%s">login</a> instead?'
                % url_for('login')
                )

