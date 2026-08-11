# 🚗 Used Car Marketplace

A backend REST API for a Used Car Marketplace built using FastAPI, MySQL, SQLAlchemy, Pydantic, and JWT authentication.

## 🚀 Features

- User registration
- Secure password hashing with bcrypt
- User login with OAuth2
- JWT authentication
- Protected car listing APIs
- Create, read, update, and delete car listings
- Owner-based authorization
- Search cars by brand and city
- Filter cars by price range
- Sort cars by price and year
- Pagination
- Pydantic request validation
- Swagger/OpenAPI documentation
- MySQL database integration
- SQLAlchemy ORM

## 🛠️ Technologies Used

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- MySQL
- JWT
- OAuth2
- Passlib / bcrypt
- Uvicorn
- Git & GitHub

## 📁 Project Structure

```text
used-car-marketplace/
│
├── routers/
│   ├── users.py
│   └── cars.py
│
├── auth.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
