from app.extensions import FlaskForm,EmailField,Length,PasswordField,InputRequired

class LoginForm(FlaskForm):
    """Form for user authentication."""
    login_email = EmailField("Email", validators=[InputRequired(), Length(max=50, message='The email must not be longer than 50 characters.')])
    login_password = PasswordField("Password", validators=[InputRequired(), Length(min=5, message='Password must be at least 5 characters.')])
   