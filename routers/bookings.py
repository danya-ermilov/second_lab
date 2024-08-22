from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth

router = APIRouter()

@router.get("/rooms/", response_model=list[schemas.Room])
def read_rooms(db: Session = Depends(database.get_db)):
    return crud.get_rooms(db)

@router.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.create_booking(db=db, booking=booking, user_id=current_user.id)

@router.get("/bookings/", response_model=list[schemas.Booking])
def read_user_bookings(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    return crud.get_bookings_by_user(db, user_id=current_user.id)
