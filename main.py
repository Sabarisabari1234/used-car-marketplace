from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
import crud
import models
import schemas
from database import SessionLocal, engine
from routers import cars, users
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Used Car Marketplace API")

app.include_router(cars.router)
app.include_router(users.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")









