from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title='To-Do service')

class Task(BaseModel):
    title: str
    # description: str
    completed: bool = False

tasks = {}
task_id_counter = 0

# POST /tasks: создание задачи
@app.post('/tasks')
def create_task(task: Task):
    global task_id_counter
    task_id_counter += 1
    tasks[task_id_counter] = task
    return {'id': task_id_counter, 'task': task}

# GET /tasks: получение списка всех задач.
@app.get('/tasks')
def get_tasks():
    return {'tasks': tasks}

# GET /tasks/{task_id}: получение задачи по ID
@app.get('/tasks/{task_id}')
def get_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    return {'id': task_id, 'task': tasks[task_id]}

# PUT /tasks/{task_id}: обновление задачи по ID
@app.put('/tasks/{task_id}')
def update_task(task_id: int, updated_task: Task):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    tasks[task_id] = updated_task
    return {'id': task_id, 'task': updated_task}

# DELETE /tasks/{task_id}: удаление задачи
@app.delete('/tasks/{task_id}')
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail='Task not found')
    tasks.pop(task_id)
    return {'id': task_id, 'status': 'deleted'}
