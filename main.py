from fastapi import FastAPI, HTTPException, Depends
from .database import engine, Base
from .routers import auth, bookings, admin
from . import models, schemas, crud, database, auth as authorize
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not authorize.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=authorize.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authorize.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

app.include_router(auth.router, prefix="/auth")
app.include_router(bookings.router, prefix="/user")
app.include_router(admin.router, prefix="/admin")
