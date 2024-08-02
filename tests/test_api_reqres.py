import requests
import json
from jsonschema import validate

from schemas.user_schemas import user_post, user_get, user_post_register, user_patch

url = "https://reqres.in/api"


def test_create_user_method_post():
    name = 'Jack'
    job = 'Developer'
    response = requests.post(f"{url}/users", params={'page': 2}, json={'name': name, 'job': job})
    body = response.json()
    assert response.status_code == 201
    assert body['name'] == name
    assert body['job'] == job
    validate(instance=body, schema=user_post)


def test_list_users_method_get():
    response = requests.get(f"{url}/users", params={'page': 2})
    body = response.json()
    assert response.status_code == 200
    assert "data" in body
    validate(instance=body, schema=user_get)


def test_update_user_method_put():
    user_id = 2
    payload = {'name': 'Jack', 'job': 'Developer'}
    response = requests.put(f"{url}/users/{user_id}", data=json.dumps(payload),
                            headers={"Content-Type": "application/json"})
    body = response.json()
    assert response.status_code == 200
    assert body['job'] == 'Developer'


def test_delete_user_method_delete():
    user_id = 2
    response = requests.delete(f"{url}/users/{user_id}")
    assert response.status_code == 204
    assert response.text == ''


def test_positive_register_user_method_post():
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    response = requests.post(f"{url}/register", json={'email': email, 'password': password})
    body = response.json()
    assert response.status_code == 200
    assert 'id' in body
    assert 'token' in body
    validate(instance=body, schema=user_post_register)


def test_negative_single_user_method_get():
    user_id = 23
    response = requests.get(f"{url}/users/{user_id}")
    assert response.status_code == 404


def test_successful_login_method_post():
    email = 'email'
    password = 'password'
    response = requests.post(f"{url}/login", json={'email': email, 'password': password})
    assert response.status_code == 400


def test_patch_user_method_patch():
    user_id = 2
    job = 'QA Engineer'
    name = 'Harry'
    response = requests.patch(f"{url}/users/{user_id}", json={'job': job, 'name': name})
    body = response.json()
    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(instance=body, schema=user_patch)
