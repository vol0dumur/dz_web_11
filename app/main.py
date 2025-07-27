from fastapi import FastAPI
from .routers import contacts
from .database import Base, engine

app = FastAPI(title="Contacts API", description="API for managing contacts")

Base.metadata.create_all(bind=engine)

app.include_router(contacts.router)