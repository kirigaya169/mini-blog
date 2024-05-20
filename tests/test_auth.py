import datetime
import os

from setup import client
from datetime import datetime, timedelta
import jwt


def test_user_registration():
    response = client.post('/user/register',
                           json={"name": "a", "password": "a"})
    assert response.status_code == 200
    token = response.json()['access_token']
    print('Bearer ' + token)
    response = client.post('/user/register',
                           json={'name': 'a', 'password': 'a'})
    assert response.status_code == 400
    response = client.delete('/user/delete',
                             headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200


def test_user_login():
    client.post('/user/register',
                json={'name': 'second', 'password': 'second'})
    response = client.post('/user/login',
                           data={'username': 'second', 'password': 'second', 'grant_type': 'password'})
    assert response.status_code == 200
    response = client.post('/user/login',
                           data={'username': 'second', 'password': 'aa', 'grant_type': 'password'})
    assert response.status_code == 403
    response = client.post('/user/login',
                           data={'username': 'aa', 'password': 'aa', 'grant_type': 'password'})
    assert response.status_code == 400


def test_jwt_auth():
    get_response = lambda current_token: client.post('/posts/', json={'header': 'aa', 'content': 'aa'},
                                                     headers={'Authorization': 'Bearer ' + current_token})
    payload = {
        'user': 'second',
        'expires': (datetime.utcnow() - timedelta(minutes=20)).strftime('%m-%y-%d %H:%M:%S')
    }
    token = jwt.encode(payload, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256')
    assert get_response(token).status_code == 401
    token = 'a'
    assert get_response(token).status_code == 401
    payload['user'] = 'third'
    payload['expires'] = (datetime.utcnow() + timedelta(minutes=20)).strftime('%m-%y-%d %H:%M:%S')
    token = jwt.encode(payload, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256')

    assert get_response(token).status_code == 400
