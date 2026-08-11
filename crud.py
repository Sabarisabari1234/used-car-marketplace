from sqlalchemy.orm import Session
import bcrypt
import models
import schemas
from fastapi import HTTPException, status

def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.User)
        .filter(models.User.email == email)
        .first()
    )

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session,login_data: schemas.UserLogin):
    db_user = get_user_by_email(db, login_data.email)

    if not db_user:
        return None

    if not bcrypt.checkpw(
        login_data.password.encode("utf-8"),
        db_user.password.encode("utf-8"),
    ):
        return None
    return db_user


def create_car(db: Session, car: schemas.CarCreate, user_id: int):
    car_data = car.model_dump()

    db_car = models.Car(
        **car_data,
        user_id=user_id
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def search_cars(db: Session,
                brand: str | None = None,
                city : str | None = None,
                min_price : int | None = None,
                max_price : int | None = None,
                sort : str | None = None,
                page : int = 1,
                limit : int = 5
                ):
    query = db.query(models.Car)

    if brand:
        query = query.filter(models.Car.brand == brand)
    if city:
        query = query.filter(models.Car.city == city)
    if min_price:
        query = query.filter(models.Car.price >= min_price)
    if max_price:
        query = query.filter(models.Car.price  <= max_price)
    if sort == "price":
        query = query.order_by(models.Car.price)
    elif sort == "-price":
        query = query.order_by(models.Car.price.desc())
    elif sort == "year":
        query = query.order_by(models.Car.year)
    elif sort == "-year":
        query = query.order_by(models.Car.year.desc())

    total = query.count()
    total_pages = (total + limit - 1) // limit
    offset = (page - 1) * limit
    cars = query.offset(offset).limit(limit).all()

    return {
        "total" : total,
        "page" : page,
        "limit" : limit,
        "total_pages" : total_pages,
        "cars" : cars
    }


def get_cars(db: Session):
    return db.query(models.Car).all()


def get_car(db: Session,car_id: int):
    return (
        db.query(models.Car)
        .filter(models.Car.id == car_id)
        .first()
    )


def update_car(db: Session,car_id: int, car: schemas.CarUpdate, user_id: int):
    db_car = get_car(db, car_id)

    if not db_car:
        return None

    if db_car.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this car"
        )

    update_data = car.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session,car_id: int, user_id : int):
    db_car = get_car(db, car_id)

    if not db_car:
        return None

    if db_car.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this car"
        )
    db.delete(db_car)
    db.commit()
    return db_car

def update_car_image(db: Session, car_id: int, image_path: str):
    car = db.query(models.Car).filter(models.Car.id == car_id).first()

    if not car:
        return None

    car.image_path = image_path
    db.commit()
    db.refresh(car)
    return car







