from wtforms import StringField, PasswordField, validators, Form


class RegistrationForm(Form):
    email = StringField("E-mail", [validators.DataRequired(message="E-mail field is required"),
                                   validators.Email(message="E-mail must be in form: foo@bar.com")])
    password = PasswordField("Password", [validators.DataRequired(message="Password field is required"),
                                          validators.EqualTo("confirm", message="Password fields must match")])
    confirm = PasswordField("Repeat password", [validators.DataRequired(message="Repeat password field is required")])


class LoginForm(Form):
    email = StringField("E-mail", [validators.DataRequired(message="E-mail field is required"),
                                   validators.Email(message="E-mail must be in form: foo@bar.com")])
    password = PasswordField("Password", [validators.DataRequired(message="Password field is required")])


class ResetPasswordForm(Form):
    password = PasswordField("New password", [validators.DataRequired(message="New password field is required"),
                                              validators.EqualTo("confirm", message="Password fields must match")])
    confirm = PasswordField("Repeat new password",
                            [validators.DataRequired(message="Repeat new password field is required")])
