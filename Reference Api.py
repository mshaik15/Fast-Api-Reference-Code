from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4

# Create FastAPI instance
app = FastAPI()

# Task data model using Pydantic
class Task(BaseModel):
    id: Optional[UUID] = None         # Unique task ID, generated automatically
    title: str                        # Task title (required)
    description: Optional[str] = None # Optional description
    completed: bool = False           # Completion status

# In-memory list to store tasks (acts like a temporary DB)
tasks = []

# POST /tasks/ - Create a new task
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    task.id = uuid4()       # Assign a unique ID
    tasks.append(task)      # Add to in-memory list
    return task             # Return created task

# GET /tasks/ - Get all tasks
@app.get("/tasks/", response_model=List[Task])
def read_tasks():
    return tasks

# GET /tasks/{task_id} - Get a specific task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

# PUT /tasks/{task_id} - Update a specific task
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: UUID, task_update: Task):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            # Use Pydantic's .copy(update={...}) to update only provided fields
            updated_task = task.copy(update=task_update.dict(exclude_unset=True))
            tasks[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

# DELETE /tasks/{task_id} - Delete a specific task
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: UUID):
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            return tasks.pop(idx)
    raise HTTPException(status_code=404, detail="Task not found")

# Launch development server if run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)