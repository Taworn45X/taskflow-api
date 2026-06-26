# TaskFlow API

A small RESTful to-do API built with **FastAPI** and **SQLite**, containerized with **Docker**.

I built this as a focused practice project to keep my backend/REST and Docker skills sharp
alongside my main computer-vision work.

## Features

- REST CRUD for tasks (`create / read / list / update / delete`)
- Filtering by completion state and priority
- Request validation with Pydantic (empty titles → `422`)
- Auto-generated OpenAPI docs at `/docs`
- SQLite persistence via SQLModel
- Dockerfile + docker-compose with a healthcheck
- pytest test suite running against an isolated in-memory DB

## Tech stack

| Layer    | Choice                |
|----------|-----------------------|
| Language | Python 3.12           |
| Framework| FastAPI               |
| ORM      | SQLModel (SQLAlchemy) |
| Database | SQLite                |
| Tests    | pytest + TestClient   |
| Runtime  | Docker / docker-compose |

## API

| Method | Path               | Description                         |
|--------|--------------------|-------------------------------------|
| GET    | `/health`          | Liveness check                      |
| GET    | `/api/tasks`       | List tasks (`?done=`, `?priority=`) |
| POST   | `/api/tasks`       | Create a task                       |
| GET    | `/api/tasks/{id}`  | Get one task                        |
| PATCH  | `/api/tasks/{id}`  | Partial update / mark done          |
| DELETE | `/api/tasks/{id}`  | Delete a task                       |

## Run locally

```bash
python -m venv .venv && source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
# open http://localhost:8000/docs
```

## Run with Docker

```bash
docker compose up --build
# API on http://localhost:8000
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest -v
```

## Example

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Write report", "priority": "high"}'

curl http://localhost:8000/api/tasks?priority=high
```

## License

MIT — see [LICENSE](LICENSE).
