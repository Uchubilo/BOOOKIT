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
