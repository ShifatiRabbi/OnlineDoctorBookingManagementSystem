# ODBMS — Online Doctor Booking Management System (Windows Dev Setup)

This repo contains two apps:
- `backend/` — Django 5 + DRF + Channels + Celery
- `frontend/` — Next.js (React + TypeScript + Tailwind)

> Recommended path on Windows: **WSL2 + Docker Desktop** (for Redis/PostgreSQL) for parity with Linux servers.  
> A native Windows path is also documented.

## Quick Start (TL;DR)
1) **Install prerequisites** (choose WSL+Docker _or_ native Windows):
   - **WSL2 + Docker Desktop** (recommended), **Git**, **Node.js LTS (20+)**, **Python 3.12+**
2) **Clone & Git**:
   ```powershell
   git clone <your-remote> ODBMS
   cd ODBMS
   git config user.name "Your Name"
   git config user.email "you@example.com"
   ```
3) **Database & Redis** (Docker path):
   ```powershell
   docker run -d --name odbms-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=odbms -p 5432:5432 postgres:16
   docker run -d --name odbms-redis -p 6379:6379 redis:7
   ```
4) **Backend**:
   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   copy .env.example .env
   # Edit .env: DATABASE_URL, REDIS_URL, SECRET_KEY
   python -m django startproject config .
   # Add settings per backend/README.md
   python manage.py migrate
   python manage.py createsuperuser
   # Run web (ASGI), Celery worker & beat:
   daphne -b 0.0.0.0 -p 8000 config.asgi:application
   celery -A config worker -l info
   celery -A config beat -l info
   ```
5) **Frontend**:
   ```powershell
   cd ../frontend
   npm create next-app@latest . -- --ts --eslint --tailwind --app --src-dir --import-alias "@/*"
   npm install @tanstack/react-query axios zod framer-motion next-i18next clsx
   # Optional UI kit:
   # npx shadcn@latest init
   # npx shadcn@latest add button card input
   echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
   npm run dev
   ```

> Full step-by-step with code snippets is in `backend/README.md` and `frontend/README.md`.
