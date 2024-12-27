import json
import os
import sys
from datetime import date

class App:
    def __init__(self):
        self.commands = {}

    def command(self, func):
        self.commands[func.__name__] = func
        return func

    def run(self, command_name, *args):
        if command_name in self.commands:
            self.commands[command_name](*args)


app = App()



todos_list = "todos_list.json"

def load_checker():
    if not os.path.exists(todos_list): 
          return []
    else: 
        with open(todos_list, "r") as archive:
            return json.load(archive)
        
def write(tasks):
    with open(todos_list, "w") as a:
        json.dump(tasks, a, indent=4)        

@app.command
def add(description):
    tasks = load_checker()
    task_id = len(tasks) + 1
    createdAt = date.today()
    updatedAt = date.today()
    task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": str(createdAt),
        "updatedAt": str(updatedAt)
    }
    tasks.append(task)
    write(tasks)
    print(f"task ID {task_id} successfully created!")

@app.command
def update(id, description): 
    tasks = load_checker()
    updateNew = str(date.today())
    id = int(id)
    for task in tasks: 
        if task["id"] == id: 
            task["description"] = description
            task["updatedAt"] = updateNew
            print("task updated successfully")
    write(tasks)

@app.command
def change(id, status): 
    tasks = load_checker()
    id = int(id)
    if status.lower() in ["todo", "in-progress", "done"]: 
        for task in tasks: 
            if task["id"] == id: 
                task["status"] = status
                task["updatedAt"] = str(date.today())
                write(tasks)
                print(f"Task ID {id} status updated successfully")
                return
    else:
        print("error, please enter a valid status")
        
    print("error, task id not found")
    
@app.command
def list_tasks(status=None): 
    tasks = load_checker()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
        print(json.dumps(tasks, indent=4))
    else: 
        for task in tasks:
            print(json.dumps(task, indent=4))
        return
    
@app.command
def delete(id):
    tasks = load_checker()
    id = int(id)
    tasks_new = [task for task in tasks if task["id"] != id]
    write(tasks_new)
    print(f"Task ID {id} deleted")

if __name__  == '__main__':
    command = sys.argv[1]
    args = sys.argv[2:]

    app.run(command, *args)