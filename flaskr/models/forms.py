from wtforms import StringField, PasswordField, validators, Form


class RegistrationForm(Form):
    """
    Class that represents the registration form used in registration.html

    Attributes:
        email : The field where the user enters the email address
        password : The field where the user enters the password
        confirm : The field where the user repeats the password
    """
    email = StringField("E-mail", [validators.DataRequired(message="E-mail field is required"),
                                   validators.Email(message="E-mail must be in form: foo@bar.com")])
    password = PasswordField("Password", [validators.DataRequired(message="Password field is required"),
                                          validators.EqualTo("confirm", message="Password fields must match")])
    confirm = PasswordField("Repeat password", [validators.DataRequired(message="Repeat password field is required")])


class LoginForm(Form):
    """
    Class that represents the login form used in login.html

    Attributes:
        email : The field where the user enters the email address
        password : The field where the user enters the password
    """
    email = StringField("E-mail", [validators.DataRequired(message="E-mail field is required"),
                                   validators.Email(message="E-mail must be in form: foo@bar.com")])
    password = PasswordField("Password", [validators.DataRequired(message="Password field is required")])


class ResetPasswordForm(Form):
    """
    Class that represents the reset password form used in reset_password.html

    Attributes:
        password : The field where the user enters the password
        confirm : The field where the user repeats the password
    """
    password = PasswordField("New password", [validators.DataRequired(message="New password field is required"),
                                              validators.EqualTo("confirm", message="Password fields must match")])
    confirm = PasswordField("Repeat new password",
                            [validators.DataRequired(message="Repeat new password field is required")])


class ForgotPasswordForm(Form):
    """
    Class that represents the forgot password form used in forgot_password.html

    Attributes:
        email : The field where the user enters the email address
    """
    email = StringField("E-mail", [validators.DataRequired(message="E-mail is required"),
                                   validators.Email(message="E-mail must be in form: foo@bar.com")])
