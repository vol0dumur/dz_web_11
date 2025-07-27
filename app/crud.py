from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta, date

from . import models, schemas

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session):
    return db.query(models.Contact).all()

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactCreate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    contact = get_contact(db, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

def search_contacts(db: Session, query: str):
    return db.query(models.Contact).filter(
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(db: Session):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)

    today_base = date(2000, today.month, today.day)
    next_week_base = date(2000, next_week.month, next_week.day)

    return db.query(models.Contact).filter(
        models.Contact.birthday != None,
        or_(
            models.Contact.birthday.between(today_base, next_week_base),
            # handle year-end wraparound
            (
                today.month == 12 and db.query(models.Contact).filter(
                    models.Contact.birthday.between(date(2000, 12, today.day), date(2000, 12, 31))
                ).exists()
            ),
            (
                next_week.month == 1 and db.query(models.Contact).filter(
                    models.Contact.birthday.between(date(2000, 1, 1), date(2000, 1, next_week.day))
                ).exists()
            )
        )
    ).all()