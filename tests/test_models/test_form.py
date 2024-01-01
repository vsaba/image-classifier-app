from flaskr.models import forms


def test_registration_form_valid():
    form = forms.RegistrationForm(email="testUser@test.hr", password="1234", confirm="1234")
    assert form.validate()


def test_registration_form_not_valid():
    form1 = forms.RegistrationForm(email="testUser_test.hr", password="1234", confirm="1234")
    assert not form1.validate()
    form2 = forms.RegistrationForm(email="testUser@test.hr", password="1234", confirm="")
    assert not form2.validate()
    form3 = forms.RegistrationForm(email="testUser@test.hr", password="1234", confirm="234")
    assert not form3.validate()


def test_login_form_valid():
    form = forms.LoginForm(email="testUser@email.com", password="1234")
    assert form.validate()


def test_login_form_not_valid():
    form1 = forms.LoginForm(email="testUser_mail.com", password="1234")
    assert not form1.validate()
    form2 = forms.LoginForm(email="testUser@gmail.com")
    assert not form2.validate()
    form3 = forms.LoginForm(password="1234")
    assert not form3.validate()


def test_forgot_password_form_valid():
    form = forms.ForgotPasswordForm(email="testUser@email.com")
    assert form.validate()


def test_forgot_password_form_not_valid():
    form1 = forms.ForgotPasswordForm(email="testUser_mail.com")
    assert not form1.validate()
    form2 = forms.ForgotPasswordForm()
    assert not form2.validate()


def test_reset_password_form_valid():
    form = forms.ResetPasswordForm(password="1234", confirm="1234")
    assert form.validate()


def test_reset_password_form_not_valid():
    form1 = forms.ResetPasswordForm(confirm="1234")
    assert not form1.validate()
    form2 = forms.ResetPasswordForm(password="1234", confirm="123")
    assert not form2.validate()
    form3 = forms.ResetPasswordForm(password="123", confirm="1234")
    assert not form3.validate()
    form4 = forms.ResetPasswordForm(password="1234")
    assert not form4.validate()
