import json

from setup import client


def test_post_creation():
    token = client.post('/user/register',
                        json={"name": "a", "password": "a"}).json()['access_token']
    response = client.post('/posts/', json={'header': 'aa', 'content': 'aa'},
                           headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert response.json()['like_count'] == 0
    response = client.get('/posts?limit=10')
    assert response.status_code == 200
    assert response.json()[0]['comments_count'] == 0
    response = client.get('/posts/user/a?limit=10', headers={'Authorization': 'Bearer ' + token})
    print(response.json())
    assert response.json()[0]['comments_count'] == 0


def test_add_like():
    token = (client.post('/user/login',
                         data={'username': 'a', 'password': 'a', 'grant_type': 'password'})
            .json()['access_token'])
    response = client.post('/posts/add_like/1',
                           headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    response = client.post('/posts/add_dislike/1',
                           headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    response = client.post('/posts/add_like/2',
                           headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 400
    response = client.post('/posts/add_like/1',
                           headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 400
    response = client.get('/posts?limit=10')
    assert response.json()[0]['like_count'] == 1

def test_add_comments():
    token = (client.post('/user/login',
                         data={'username': 'a', 'password': 'a', 'grant_type': 'password'})
    .json()['access_token'])
    response = client.post('/posts/add_comment/1',
                           headers={'Authorization': 'Bearer ' + token},
                           json={'comment': 'aa'})
    assert response.status_code == 200
    response = client.post('/posts/add_comment/2',
                           headers={'Authorization': 'Bearer ' + token},
                           json={'comment': 'aa'})
    assert response.status_code == 400


def test_get_post_info():
    token = (client.post('/user/login',
                         data={'username': 'a', 'password': 'a', 'grant_type': 'password'})
    .json()['access_token'])
    response = client.get('/posts/2', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 400
    response = client.get('/posts/1', headers={'Authorization': 'Bearer ' + token})
    assert response.status_code == 200
    assert response.json() == json.loads('''{
      "id": 1,
      "header": "aa",
      "content": "aa",
      "likes": [
        {
          "id": 2,
          "username": "a"
        }
      ],
      "dislikes": [
        {
          "id": 2,
          "username": "a"
        }
      ],
      "comments": [
        {
          "username": "a",
          "comment": "aa"
        }
      ]
    }''')