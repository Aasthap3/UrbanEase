from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest


class DuplicateEmailError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


def register_user(db: Session, request: RegisterRequest) -> User:
    existing_user = db.scalar(select(User).where(User.email == request.email))
    if existing_user is not None:
        raise DuplicateEmailError

    user = User(
        name=request.name,
        email=request.email,
        password_hash=hash_password(request.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateEmailError from exc
    db.refresh(user)
    return user


def authenticate_user(db: Session, request: LoginRequest) -> str:
    user = db.scalar(select(User).where(User.email == request.email))
    if user is None or not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError
    return create_access_token({'sub': str(user.id)})