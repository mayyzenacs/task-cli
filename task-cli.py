import json
import os
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
def new_task(tasks):
    description = input("Enter a description to your task " )
    task_id = len(tasks) + 1
    createdAt = date.today()
    updatedAt = date.today()
    task = {
        "id": task_id,
        "description": description,
        "status": "To-Do",
        "createdAt": str(createdAt),
        "updatedAt": str(updatedAt)
    }
    tasks.append(task)
    print(f"task ID{task_id} successfully created!")

@app.command
def update_task(tasks): 
    id = int(input("Enter the task ID you want to change: ").strip( ))
    description = input("Enter a description: ")
    updateNew = date.today()
    for task in tasks: 
        if task["id"] == id: 
            task["description"] = description
            task["updatedAt"] = updateNew
            print("task updated successfully")
    write(tasks)

@app.command
def change_status(tasks): 
    id = int(input("Task id that you want to change "))
    status = input("new status: ").strip().lower()
    if status == "done" or "in-progress": 
        for task in tasks: 
            if task["id"] == id: 
                task["status"] = status
                write(tasks)
                print(f"Task ID {id} status updated successfully")
            else:
                print("task not found")
                return
    else:
        print("error, please enter a valid status")
        return
    
@app.command
def list_tasks(status=None): 
    tasks = load_checker()
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    else: 
        for task in tasks:
            print(json.dumps(task, indent=4))


def main():
    list = load_checker()
    while True:
        print("CLI Task Tracker")
        print( """
            1 - Add new task
            2 - Update task
            3 - Delete task
            4 - Change task status
            5 - View tasks
            6 - Exit
            """)


        option = int(input("Choose an menu option "))
        if option == 1:
            new_task(list)
            write(list)
        elif option == 2:
            update_task(list)
        elif option == 3:
            pass
        elif option == 4:
            change_status(list)
        elif option == 5:
            choose = input("Choose task status to filter [todo, in-progress, done] or leave empty to show all ").strip().lower()
            if choose not in ["todo", "in-progress", "done", ""]: 
                print("invalid, choose a valid task status ")
                continue
            list_tasks(choose if choose else None)
        elif option == 6: 
            print("Goodbye!")
            break
        else: 
            print("Invalid number")
            continue

main()

if __name__ == "__main__":
    main()