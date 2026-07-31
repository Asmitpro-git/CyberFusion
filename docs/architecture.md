# Architecture Overview

## Module 1 Goals

Module 1 establishes the infrastructure needed for a secure enterprise platform while avoiding domain logic that belongs to later delivery phases.

## Backend Layer

- FastAPI application factory in `backend/app/main.py`.
- Centralized configuration in `backend/app/config/settings.py`.
- Request ID and timing middleware in `backend/app/middleware/`.
- SQLAlchemy engine and session management in `backend/app/database/`.
- Alembic migration scaffold in `backend/alembic/`.

## Frontend Layer

- React 19 application in `frontend/src/`.
- Route-driven shell with a shared layout.
- Sidebar and topbar foundation for SOC-style operations.
- Tailwind-based dark theme with glassmorphism styling.

## Container Layer

- PostgreSQL 16 runs as the persistence layer.
- Backend container serves the FastAPI API.
- Frontend container serves the SPA through Nginx.
- Docker Compose orchestrates local development and deployment parity.

## Operating Principles

- Keep core platform concerns separated by layer.
- Avoid mixing UI presentation with infrastructure policy.
- Preserve room for future modules without rewriting the foundation.