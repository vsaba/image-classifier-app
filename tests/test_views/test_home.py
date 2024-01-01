def test_home_good(test_client):
    response = test_client.get('/home/', follow_redirects=True)

    assert response.status_code == 200
    assert b'Hello! Welcome to the Image classifier app!' in response.data


def test_home_logout_required(test_client, login_default_user):
    response = test_client.get('/home/', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == '/home/app'


def test_app_good(test_client, login_default_user):
    response = test_client.get('/home/app', follow_redirects=True)

    assert response.status_code == 200
    assert b'Predict!' in response.data


def test_app_login_required(test_client):
    response = test_client.get('/home/app', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == '/auth/login'


def test_random_image_all_good(test_client):
    response = test_client.get('/home/random', headers={
        'X-Requested-With': 'XMLHttpRequest',
    })

    assert response.json["image_url"] is not None


def test_random_image_invalid_call(test_client, login_default_user):
    response = test_client.get('/home/random', follow_redirects=True)

    assert len(response.history) == 1
    assert response.request.path == "/home/app"


def test_predict_image_valid(test_client):
    response = test_client.post('/home/predict', json={
        "imagePath": "images/img_1.jpg"
    })

    assert response.json["prediction"] is not None


def test_predict_image_invalid_uri(test_client):
    response = test_client.post('/home/predict', json={
        "imagePath": "images/incorrect_image_path"
    }, follow_redirects=True)

    assert response.json is None


def test_inactive_not_verified(test_client, init_db):
    test_client.post('/auth/login', data=dict(email="userNotVerified@gmail.com", password="1234"))
    response = test_client.get('/home/inactive', follow_redirects=True)

    assert b'Email verification required!' in response.data
