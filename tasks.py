from celery import Celery
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models
from .celery_app import celery_app
from time import sleep

@celery_app.task
def remove_booking_after_end(booking_id: int, end_time: str):
    print(f"Task started for booking ID {booking_id}")

    end_time_dt = datetime.fromisoformat(end_time)
    wait_time = (end_time_dt - datetime.utcnow()).total_seconds()

    if wait_time > 0:
        print(f"Waiting for {wait_time} seconds until booking expires")
        sleep(wait_time)  

    db: Session = SessionLocal()
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()

    if db_booking:
        print(f"Deleting booking ID {booking_id}")
        db.delete(db_booking)
        db.commit()
    else:
        print(f"Booking ID {booking_id} not found")

    db.close()
    print(f"Task completed for booking ID {booking_id}")
