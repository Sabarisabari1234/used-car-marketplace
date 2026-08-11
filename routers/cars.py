from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
import os
import shutil
import uuid
import auth
import models

router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)

@router.post("/", response_model=schemas.CarResponse, status_code=status.HTTP_201_CREATED,)
def create_car(car: schemas.CarCreate,db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_car(db, car, current_user.id)

@router.get("/", response_model=list[schemas.CarResponse])
def get_cars(db: Session = Depends(get_db)):
    return crud.get_cars(db)

@router.get("/search", response_model=schemas.CarListResponse)
def search_cars(
        brand: str | None = None,
        city : str | None = None,
        min_price : int | None = None,
        max_price : int | None = None,
        sort : str | None = None,
        page : int = Query(default=1, ge=1),
        limit : int = Query(default=5, ge=5, le=50),
        db: Session = Depends(get_db)
):
    cars = crud.search_cars(db, brand, city, min_price, max_price, sort, page, limit)
    return cars


@router.get("/{car_id}", response_model=schemas.CarResponse)
def get_car(car_id: int,db: Session = Depends(get_db),):
    car = crud.get_car(db, car_id)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found",
        )

    return car

@router.put("/{car_id}",response_model=schemas.CarResponse)
def update_car(car_id: int, car: schemas.CarUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    updated_car = crud.update_car(db, car_id, car, current_user.id)

    if not updated_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found",
        )
    return updated_car

@router.delete("/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    deleted_car = crud.delete_car(db, car_id, current_user.id)

    if not deleted_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found",
        )
    return {
        "message": "Car deleted successfully"
    }

@router.post("/{car_id}/upload-image")
async def upload_car_image(car_id: int,image: UploadFile = File(...), db: Session = Depends(get_db)):
    unique_filename = f"{uuid.uuid4()}-{image.filename}"
    file_path = f"uploads/{unique_filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    updated_car = crud.update_car_image(db, car_id, file_path)

    if not updated_car:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return {
        "message": "Image uploaded successfully",
        "car_id": updated_car.id,
        "image_path": updated_car.image_path
    }