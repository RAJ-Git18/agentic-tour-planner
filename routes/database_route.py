from fastapi import APIRouter, Depends
from dependencies.dependency import get_db
from sqlalchemy.orm import Session
from models.models import User, Booking

router = APIRouter(tags=["Database"])

@router.get("/get_user_db")
def get_user_db(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users
@router.get("/get_booking_db")
def get_booking_db(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings
@router.delete("/delete_booking_db")
def delete_booking_db(db: Session = Depends(get_db)):
    db.query(Booking).delete()
    db.commit()
    return {"message": "Booking deleted successfully."}
    
