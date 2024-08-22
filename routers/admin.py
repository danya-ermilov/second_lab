from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud, database, auth

router = APIRouter()

@router.post("/rooms/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate, db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.create_room(db=db, room=room)

@router.get("/bookings/", response_model=list[schemas.Booking])
def read_all_bookings(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(auth.get_current_admin)):
    return crud.get_all_bookings(db)
