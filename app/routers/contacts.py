from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from ..database import SessionLocal

router = APIRouter(prefix="/contacts", tags=["Contacts"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.ContactResponse)
def create(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@router.get("/", response_model=List[schemas.ContactResponse])
def read_all(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def read(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=schemas.ContactResponse)
def update(contact_id: int, contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    db_contact = crud.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}")
def delete(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.delete_contact(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@router.get("/search/", response_model=List[schemas.ContactResponse])
def search(query: str, db: Session = Depends(get_db)):
    return crud.search_contacts(db, query)

@router.get("/birthdays/", response_model=List[schemas.ContactResponse])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)