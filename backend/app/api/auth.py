from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import (
    DuplicateEmailError,
    InvalidCredentialsError,
    authenticate_user,
    register_user,
)

router = APIRouter(prefix='/auth', tags=['authentication'])


@router.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)) -> User:
    try:
        return register_user(db, request)
    except DuplicateEmailError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is already registered') from None


@router.post('/login', response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    try:
        access_token = authenticate_user(db, request)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        ) from None
    return TokenResponse(access_token=access_token)


@router.get('/me', response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)) -> User:
    return current_user