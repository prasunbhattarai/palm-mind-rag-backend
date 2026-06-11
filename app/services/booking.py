from datetime import date, time

from app.db.postgres import SessionLocal
from app.db.models import Booking


def create_booking(name: str, email: str, interview_date: str, interview_time: str):
    try:
        parsed_date = date.fromisoformat(interview_date)
        parsed_time = time.fromisoformat(interview_time)
    except ValueError:
        return {"status": "error", "message": "Invalid date or time format"}

    db = SessionLocal()
    try:
        booking = Booking(
            name=name,
            email=email,
            interview_date=parsed_date,
            interview_time=parsed_time,
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return {
            "id": booking.id,
            "name": booking.name,
            "email": booking.email,
            "date": interview_date,
            "time": interview_time,
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
