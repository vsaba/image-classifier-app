from flaskr.util import token


def test_register_valid_user_valid_token(test_client, init_db):
    response = test_client.post('/auth/register',
                                data=dict(email="test@gmail.com", password="1234", confirm="1234"),
                                follow_redirects=True)
    assert response.request.path == "/home/inactive"

    ver_token = token.generate_token("test@gmail.com")
    response = test_client.get('/auth/verify/' + ver_token, follow_redirects=True)

    assert response.request.path == "/home/app"

    test_client.get('/auth/logout')


def test_register_valid_user_invalid_token(test_client, init_db):
    response = test_client.post('/auth/register', data=dict(email="test1@gmail.com", password="1234", confirm="1234"),
                                follow_redirects=True)
    assert response.request.path == "/home/inactive"

    nonce_token = "46453241"
    response = test_client.get('/auth/verify/' + nonce_token, follow_redirects=True)

    assert b'An error occurred while verifying.' in response.data
    assert response.request.path == "/home/inactive"

    test_client.get('/auth/logout')


def test_register_user_exists(test_client, init_db):
    response = test_client.post('/auth/register',
                                data=dict(email="userVerified@gmail.com", password="1234", confirm="1234"),
                                follow_redirects=True)
    assert b'Provided email is already in use' in response.data


def test_register_get(test_client):
    response = test_client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register here:' in response.data


def test_register_logout_required(test_client, init_db, login_default_user):
    response = test_client.get('/auth/register', follow_redirects=True)
    assert len(response.history) == 1
    assert response.request.path == '/home/app'


def test_login_valid(test_client, init_db):
    response = test_client.post('/auth/login', data=dict(email="userVerified@gmail.com", password="1234"),
                                follow_redirects=True)

    assert b'Successfully logged in!' in response.data
    assert response.request.path == '/home/app'

    test_client.get('/auth/logout')


def test_login_not_valid(test_client, init_db):
    response = test_client.post('/auth/login', data=dict(email="userNotExists@gmail.com", password="1234"),
                                follow_redirects=True)
    assert b'Credentials are incorrect' in response.data

    response = test_client.post('/auth/login', data=dict(email="userVerified@gmail.com", password="wrong password"),
                                follow_redirects=True)

    assert b'Credentials are incorrect' in response.data


def test_login_get_valid(test_client):
    response = test_client.get('/auth/login', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login here:' in response.data


def test_login_logout_required(test_client, login_default_user):
    response = test_client.get('/auth/login', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/home/app"


def test_logout_valid(test_client, login_default_user):
    response = test_client.get('/auth/logout', follow_redirects=True)

    assert b'Logged out successfully!' in response.data
    assert len(response.history) == 1
    assert response.request.path == "/home/"


def test_logout_login_required(test_client):
    response = test_client.get('/auth/logout', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/auth/login"


def test_verify_email_already_verified(test_client, login_default_user):
    response = test_client.get('/auth/verify/123432', follow_redirects=True)

    assert b'You have already verified your email address' in response.data
    assert len(response.history) == 1
    assert response.request.path == "/home/app"


def test_forgot_password_email_good(test_client, init_db):
    response = test_client.post('/auth/forgot', data=dict(email="userVerified@gmail.com"), follow_redirects=True)

    assert b'Email with link for password reset sent.' in response.data
    assert len(response.history) == 1
    assert response.request.path == '/home/'


def test_forgot_password_email_incorrect(test_client, init_db):
    response = test_client.post('/auth/forgot', data=dict(email="userNotExists@gmail.com"), follow_redirects=True)

    assert b'Email invalid. Please try again.' in response.data


def test_forgot_password_get(test_client):
    response = test_client.get('/auth/forgot', follow_redirects=True)

    assert response.status_code == 200
    assert b'Forgot password' in response.data


def test_forgot_password_logout_required(test_client, login_default_user):
    response = test_client.get('/auth/forgot', follow_redirects=True)

    assert b'You are already logged in' in response.data
    assert len(response.history) == 1
    assert response.request.path == '/home/app'


def test_reset_password_token_valid(test_client):
    ver_token = token.generate_token("userVerified@gmail.com")

    response = test_client.get('/auth/reset/' + ver_token, follow_redirects=True)

    assert b'Reset password' in response.data


def test_reset_password_token_not_valid(test_client):
    ver_token = token.generate_token("userVerified@gmail.com")

    response = test_client.get('/auth/reset/473573458743', follow_redirects=True)

    assert b'An error occurred while validating.' in response.data
    assert len(response.history) == 1
    assert response.request.path == '/auth/forgot'


def test_reset_password_successful(test_client, init_db):
    ver_token = token.generate_token("userVerified@gmail.com")

    response = test_client.post('/auth/reset/' + ver_token, data=dict(password="12345", confirm="12345"),
                                follow_redirects=True)

    assert b'Password successfully changed!' in response.data
    assert len(response.history) == 1
    assert response.request.path == '/home/'
