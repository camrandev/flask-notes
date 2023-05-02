from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email


class RegisterForm(FlaskForm):
    """Form for user registration"""

    username = StringField(
        "User Name",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)]
    )

    email = EmailField(
        "Email",
        validators=[InputRequired(), Length(max=50), Email()]
    )
    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=30)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=30)]
    )


class LoginForm(FlaskForm):
    """form for user to login"""

    username = StringField(
        "User Name",
        validators=[InputRequired(), Length(max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(max=100)]
    )

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""

