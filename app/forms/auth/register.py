from app.extensions import FlaskForm,EmailField,Length,PasswordField,InputRequired,StringField,EqualTo

class RegisterForm(FlaskForm):
    """Form for user registration."""

    register_first_name = StringField("First Name", validators=[InputRequired(), Length(min=2, max=50, message='First name must be between 2 and 50 characters.')])
    register_last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=50, message='Last name must be between 2 and 50 characters.')])
    register_email = EmailField("Email", validators=[InputRequired(), Length(max=50, message='The email must not be longer than 50 characters.')])
    register_password = PasswordField("Password", validators=[InputRequired(), Length(min=5, message='Password must be at least 5 characters.')])
    register_password_confirm = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('register_password', message='Passwords must match.')])