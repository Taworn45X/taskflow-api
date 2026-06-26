# TaskFlow API

โปรเจกต์เล็กๆ ที่ผมทำไว้ฝึกเขียน REST API กับลองใช้ Docker ครับ เป็น API จัดการรายการงาน (to-do)
ง่ายๆ เพิ่ม/ลบ/แก้/ดูงานได้ ทำด้วย FastAPI + SQLite

ปกติงานหลักผมทำสาย computer vision เลยอยากมีโปรเจกต์ backend ไว้ฝึกมือไม่ให้ลืม 555

## มันทำอะไรได้บ้าง

- เพิ่มงาน / ดูงานทั้งหมด / ดูงานทีละอัน / แก้ไข / ลบ
- กรองงานตามความสำคัญ (priority) หรือกรองเฉพาะงานที่ทำเสร็จแล้ว
- มีเช็คข้อมูลก่อนบันทึก (ใส่ title ว่างไม่ได้)
- เข้า `/docs` แล้วลองยิง API ได้เลยผ่าน Swagger
- รันผ่าน Docker ได้

## ที่ใช้ทำ

Python 3.12 · FastAPI · SQLModel (SQLite) · pytest · Docker

## เส้นทาง (endpoints)

| Method | Path | ทำอะไร |
|--------|------|--------|
| GET | `/health` | เช็คว่าเซิร์ฟเวอร์ยังอยู่ |
| GET | `/api/tasks` | ดูงานทั้งหมด (ใส่ `?done=` `?priority=` กรองได้) |
| POST | `/api/tasks` | เพิ่มงานใหม่ |
| GET | `/api/tasks/{id}` | ดูงานอันเดียว |
| PATCH | `/api/tasks/{id}` | แก้งาน / ติ๊กว่าเสร็จ |
| DELETE | `/api/tasks/{id}` | ลบงาน |

## วิธีรัน (แบบปกติ)

```bash
python -m venv .venv
.venv\Scripts\activate            # ถ้าเป็น mac/linux ใช้ source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

เสร็จแล้วเปิด http://localhost:8000/docs

## วิธีรัน (Docker)

```bash
docker compose up --build
```

## รันเทส

```bash
pip install -r requirements-dev.txt
pytest -v
```

## ลองยิงดู

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"อ่านหนังสือสอบ\", \"priority\": \"high\"}"
```

---

## English (short version)

A small to-do REST API I built to practice backend development and Docker.
My main work is in computer vision, so this is a side project to keep my REST/API
skills fresh. Built with **FastAPI + SQLite**, runs in **Docker**, and has a small
**pytest** suite.

- Full CRUD for tasks, with filtering by `priority` / `done`
- Input validation (empty title → `422`)
- Auto Swagger docs at `/docs`

Run locally: `uvicorn app.main:app --reload` → http://localhost:8000/docs
Run with Docker: `docker compose up --build`
Run tests: `pytest -v`

License: MIT
