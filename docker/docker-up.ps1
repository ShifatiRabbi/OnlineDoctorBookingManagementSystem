# Run Postgres and Redis via Docker (Windows PowerShell)
docker run -d --name odbms-pg -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=odbms -p 5432:5432 postgres:16
docker run -d --name odbms-redis -p 6379:6379 redis:7
