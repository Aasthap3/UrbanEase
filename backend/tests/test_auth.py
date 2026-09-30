from datetime import timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.database import SessionLocal
from app.core.security import create_access_token, verify_password
from app.main import app
from app.models.user import User

client = TestClient(app)


@pytest.fixture(autouse=True)
def remove_auth_test_users() -> None:
    yield
    with SessionLocal() as session:
        session.execute(delete(User).where(User.email.like('auth-test-%')))
        session.commit()


def registration_payload() -> dict[str, str]:
    return {
        'name': 'Auth Test User',
        'email': f'auth-test-{uuid4()}@example.com',
        'password': 'secure-password',
    }


def test_registers_user_with_hashed_password_and_safe_response() -> None:
    payload = registration_payload()

    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data['email'] == payload['email']
    assert 'password' not in response_data
    assert 'password_hash' not in response_data

    with SessionLocal() as session:
        user = session.scalar(select(User).where(User.email == payload['email']))
        assert user is not None
        assert user.password_hash != payload['password']
        assert verify_password(payload['password'], user.password_hash)


def test_registration_rejects_duplicate_email() -> None:
    payload = registration_payload()
    assert client.post('/api/auth/register', json=payload).status_code == 201

    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 409


@pytest.mark.parametrize(
    'payload',
    [
        {'name': 'Auth Test', 'email': 'not-an-email', 'password': 'secure-password'},
        {'email': 'auth-test-missing@example.com', 'password': 'secure-password'},
        {'name': 'Auth Test', 'email': 'auth-test-short@example.com', 'password': 'short'},
        {'name': '   ', 'email': 'auth-test-empty@example.com', 'password': 'secure-password'},
    ],
)
def test_registration_validates_input(payload: dict[str, str]) -> None:
    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 422


def test_login_returns_access_token() -> None:
    payload = registration_payload()
    client.post('/api/auth/register', json=payload)

    response = client.post(
        '/api/auth/login',
        json={'email': payload['email'].upper(), 'password': payload['password']},
    )

    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    assert response.json()['access_token']


@pytest.mark.parametrize(
    'email, password',
    [
        ('auth-test-missing@example.com', 'secure-password'),
        ('auth-test-wrong@example.com', 'wrong-password'),
    ],
)
def test_login_rejects_invalid_credentials(email: str, password: str) -> None:
    response = client.post('/api/auth/login', json={'email': email, 'password': password})

    assert response.status_code == 401
    assert response.json()['detail'] == 'Invalid email or password'


def test_protected_endpoint_accepts_valid_token() -> None:
    payload = registration_payload()
    client.post('/api/auth/register', json=payload)
    login_response = client.post('/api/auth/login', json=payload)

    response = client.get(
        '/api/auth/me',
        headers={'Authorization': f"Bearer {login_response.json()['access_token']}"},
    )

    assert response.status_code == 200
    assert response.json()['email'] == payload['email']


@pytest.mark.parametrize('authorization', [None, 'Bearer malformed-token'])
def test_protected_endpoint_rejects_missing_or_malformed_token(authorization: str | None) -> None:
    headers = {} if authorization is None else {'Authorization': authorization}

    response = client.get('/api/auth/me', headers=headers)

    assert response.status_code == 401


def test_protected_endpoint_rejects_expired_token() -> None:
    token = create_access_token({'sub': str(uuid4())}, expires_delta=timedelta(minutes=-1))

    response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 401


def test_protected_endpoint_rejects_token_for_nonexistent_user() -> None:
    token = create_access_token({'sub': str(uuid4())})

    response = client.get('/api/auth/me', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 401