import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

import typing as t

from app.schemas.user import UserCreate, UserOut, UserEdit, UserBase, UsermeEdit
from app.core.security import get_password_hash

from app.db.models import User

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> UserBase:
    return db.query(User).filter(User.email == email).first()


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> t.List[UserOut]:
    return db.query(User).offset(skip).limit(limit).all()


def create_supuser(db: Session, user: UserCreate):
    hashed_password = get_password_hash("admin")
    db_user = User(
        username=user.username,
        email=user.email,
        im=user.im,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user(db: Session, user: UserCreate, fonction_id: int):
    hashed_password = get_password_hash("user")
    db_user = User(
        username=user.username.title(),
        email=user.email,
        im=user.im,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
        fonction_id=fonction_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(
    db: Session, user_id: int, user: UserEdit
) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def edit_userme(
    db: Session, user_id: int, user: UsermeEdit
) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user