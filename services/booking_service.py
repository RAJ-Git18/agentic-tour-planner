from models.models import Booking
from typing import Dict
from utils.logger import logger


class BookingService:
    def __init__(self, db):
        self.db = db

    def route_booking_cancel_confirm(self, user_id: int, title: str, intent: str):
        if intent == "confirm_booking":
            return self.confirm_booking(user_id, title)
        elif intent == "cancel_booking":
            return self.cancel_booking(user_id)
        elif intent == "ask_booking":
            return self.ask_booking(user_id)

    def confirm_booking(self, user_id: int, title: str):
        booking = Booking(user_id=user_id, title=title)
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        logger.info(f"Booking created: {booking.id}")
        return {
            "status": "success",
            "booking_id": booking.id,
            "message": "Booking confirmed successfully.",
        }

    def cancel_booking(self, user_id: int):
        bookings = self.db.query(Booking).filter(Booking.user_id == user_id).all()
        count = len(bookings)
        for b in bookings:
            self.db.delete(b)
        self.db.commit()
        logger.info(f"Cancelled {count} bookings for user {user_id}")
        return {
            "status": "success",
            "message": f"Successfully cancelled {count} bookings.",
        }

    def ask_booking(self, user_id: int):
        bookings = self.db.query(Booking).filter(Booking.user_id == user_id).all()
        titles = [b.title for b in bookings]
        logger.info(f"User {user_id} has {len(bookings)} bookings: {titles}")
        return {
            "status": "success",
            "booking_titles": titles,
            "message": (
                f"You have {len(bookings)} active bookings."
                if titles
                else "You have no active bookings."
            ),
        }
