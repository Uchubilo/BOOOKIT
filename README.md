# BookIt API

A production-ready REST API for a bookings platform. Users browse services, book, and review. Admins manage everything.

## 🏗️ Architecture Decisions

- **Modular Design**: Routers → Services → Repositories (clean separation)
- **Auth**: Stateless JWT with refresh tokens; bcrypt password hashing
- **Validation**: Pydantic (request/response) + PostgreSQL constraints (DB-level integrity)
- **Booking Conflicts**: Prevented via service-layer time overlap checks
- **Soft Deletes Avoided**: Explicit status management (`cancelled`, etc.) preserves auditability

## 🗄️ Why PostgreSQL?

- **ACID-compliant** and rock-solid for transactional data (bookings, payments)
- **Rich constraints** (e.g., `CHECK(rating BETWEEN 1 AND 5)`)
- **JSON support** (future-proofing)
- **Mature tooling** with Alembic for migrations
- **Production standard** — far more robust than SQLite/MySQL for this use case

## 🚀 Local Setup

1. Create virtual env:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```


Prerequisites
Python 3.11+
PostgreSQL installed and running
Create a database:
createdb boookit
Clone & Setup git clone https://github.com//bookit.git cd boookit python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate pip install -r requirements.txt

Environment Variables

Create a .env file in the root directory:

DATABASE_URL=postgresql://bookit_user:12345@localhost:5432/bookit_db
SECRET_KEY=your-super-secret-jwt-key-change-in-prod
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

Apply Database Migrations alembic upgrade head

Start the Server uvicorn app.main:app --reload

Test the API

Open your browser at:

http://127.0.0.1:8000/docs
