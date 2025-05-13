# FastAPI User Authentication API

This project is a FastAPI-based API for user registration, login, and OTP-based email verification. It includes routes for registering users, verifying OTPs, and authenticating via JWT tokens.

## Features

- User Registration with email OTP verification
- JWT-based authentication
- Secure password hashing (bcrypt)
- SQLAlchemy ORM for database interactions
- Email service integration for OTP delivery

---

## 🔧 Setup and Installation

Follow these steps to get the project up and running locally

Create a Virtual Environment
Using venv to manage dependencies.

On Linux / MacOS:
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
Make sure you have a requirements.txt file, then run:
pip install -r requirements.txt

4️⃣ Run the FastAPI Applicatio
uvicorn main:app --reload