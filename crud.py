from sqlalchemy.orm import Session
from . import models, schemas, auth
from fastapi import HTTPException, status
import asyncio
from datetime import datetime
from .tasks import remove_booking_after_end


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_admin(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role='admin')
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_room(db: Session, room: schemas.RoomCreate):
    db_room = models.Room(name=room.name, description=room.description)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):
    # Проверяем, есть ли уже бронирование для этого user_id и room_id
    existing_booking = db.query(models.Booking).filter(
        models.Booking.user_id == user_id,
        models.Booking.room_id == booking.room_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already exists for this user and room"
        )
    
    # Создаем новое бронирование
    db_booking = models.Booking(**booking.dict(), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # Отправляем задачу в Celery
    remove_booking_after_end.apply_async(
        args=[db_booking.id, db_booking.end_time.isoformat()],
        countdown=(db_booking.end_time - datetime.utcnow()).total_seconds()
    )
    
    return db_booking
'''
def create_booking(db: Session, booking: schemas.BookingCreate, user_id: int):#, background_tasks: BackgroundTasks):
    # Проверяем, есть ли уже бронирование для этого user_id и room_id
    existing_booking = db.query(models.Booking).filter(
        models.Booking.user_id == user_id,
        models.Booking.room_id == booking.room_id
    ).first()
    
    if existing_booking:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already exists for this user and room"
        )
    
    # Создаем новое бронирование
    db_booking = models.Booking(**booking.dict(), user_id=user_id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    # Добавляем задачу для удаления бронирования по окончании
    #background_tasks.add_task(remove_booking_after_end, db, db_booking.id, db_booking.end_time)
    
    return db_booking
'''
def get_rooms(db: Session):
    return db.query(models.Room).all()

def get_bookings_by_user(db: Session, user_id: int):
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).all()

def get_all_bookings(db: Session):
    return db.query(models.Booking).all()
