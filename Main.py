from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Task Management Service",
    description="سرویس مدیریت کارها برای درس مهندسی نرم‌افزار پیشرفته",
    version="1.0.0",
)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    done: bool = False


class Task(TaskCreate):
    id: int


tasks_db: List[Task] = []


def find_task_index(task_id: int) -> int:
    for index, t in enumerate(tasks_db):
        if t.id == task_id:
            return index
    return -1


@app.get("/", summary="سلام سرویس")
def root():
    return {"message": "سرویس مدیریت کارها فعال است"}


@app.post("/tasks", response_model=Task, summary="ایجاد کار جدید")
def create_task(task: Task):
    if find_task_index(task.id) != -1:
        raise HTTPException(status_code=400, detail="شناسه کار تکراری است")
    tasks_db.append(task)
    return task


@app.get("/tasks", response_model=List[Task], summary="دریافت همه کارها")
def get_tasks():
    return tasks_db


@app.get("/tasks/{task_id}", response_model=Task, summary="دریافت یک کار")
def get_task(task_id: int):
    index = find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="کار پیدا نشد")
    return tasks_db[index]


@app.put("/tasks/{task_id}", response_model=Task, summary="ویرایش کار")
def update_task(task_id: int, updated: TaskCreate):
    index = find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="کار برای ویرایش پیدا نشد")
    new_task = Task(id=task_id, **updated.dict())
    tasks_db[index] = new_task
    return new_task


@app.delete("/tasks/{task_id}", summary="حذف کار")
def delete_task(task_id: int):
    index = find_task_index(task_id)
    if index == -1:
        raise HTTPException(status_code=404, detail="کار برای حذف پیدا نشد")
    tasks_db.pop(index)
    return {"message": "کار حذف شد"}
