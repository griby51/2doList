from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, VSplit, Window, HSplit
from prompt_toolkit.widgets import Box, Frame, Label, TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import FormattedTextControl
import json

# Charger les données depuis le fichier JSON
try :
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"lists": []}

# Styles pour l'application
style = Style.from_dict({
    "frame": "bg:#040404 fg:#106cbc",
    "box": "bg:#040404 fg:#106cbc",

    "list-undone-unselected": "bg:#040404 fg:#0b4583",
    "list-undone-selected": "bg:#106cbc fg:#05224b",
    "list-done-unselected": "bg:#040404 fg:#0b4583 strike",
    "list-done-selected": "bg:#106cbc fg:#05224b strike",

    "task-undone-unselected": "bg:#040404 fg:#0b4583",
    "task-undone-selected": "bg:#106cbc fg:#05224b",
    "task-done-unselected": "bg:#040404 fg:#0b4583 strike",
    "task-done-selected": "bg:#106cbc fg:#05224b strike",
})

kb = KeyBindings()

class List:
    def __init__(self, name, done, id, tasks):
        self.name = name
        self.done = done
        self.id = id
        self.tasks = [self.Task(task['name'], task['done'], task['index']) for i, task in enumerate(tasks)]

    class Task:
        def __init__(self, name, done, index):
            self.name = name
            self.done = done
            self.index = index
    
    def addTask(self, task_name):
        new_id = len(self.tasks)  # Index basé sur la longueur actuelle des tâches
        self.tasks.append(self.Task(task_name, False, new_id))
    
    def removeTask(self, task_id):
        self.tasks = [task for task in self.tasks if task.index != task_id]
        for task in self.tasks:
            if task.index > task_id:
                task.index -= 1

    def toDict(self):
        return {
            "name": self.name,
            "done": self.done,
            "id": self.id,
            "tasks": [
                {
                    "name": task.name,
                    "done": task.done,
                    "index": task.index
                }
                for task in self.tasks
            ]
        }

all_list = []


for _list in data["lists"]:
    all_list.append(List(_list["name"], _list["done"], _list["id"], _list["tasks"]))

if len(all_list) != 0:
    global selected_list
    selected_list = all_list[0]

def updateListArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected=None):
    formatted_text = []

    for i in all_list:
        style = done_style if i.done else not_done_style
        try:
            if i.id == selected.id:
                style = selected_done_style if i.done else selected_not_done_style
        except:
            pass
        formatted_text.append((style, i.name + "\n"))

    return FormattedTextControl(formatted_text)

def updateTaskArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected_list=None, selected_task=None):
    if selected_list is None:
        return FormattedTextControl([])  # Pas de liste sélectionnée

    formatted_text = []

    for task in selected_list.tasks:
        style = done_style if task.done else not_done_style
        if selected_task is not None:
            if task.index == selected_task.index:
                style = selected_done_style if task.done else selected_not_done_style
        formatted_text.append((style, task.name + "\n"))  # Afficher l'index

    return FormattedTextControl(formatted_text)


def addList(new_list):
    all_list.append(new_list)

def removeList(index):
    if len(all_list) != 0:
        all_list.pop(index)

selected_list = None if len(all_list) == 0 else all_list[0]
if selected_list is not None and len(selected_list.tasks) != 0:
    selected_task = selected_list.tasks[0]

def saveSelectedList():
    global selected_list
    if selected_list is not None:
        all_list[selected_list.id] = selected_list

def saveSelectedTask():
    global selected_task
    if selected_task is not None:
        selected_list.tasks[selected_task.index] = selected_task

def saveData():
    saveSelectedList()
    with open("data.json", "w") as f:
        json.dump({"lists": [i.toDict() for i in all_list]}, f)

list_area = Window(content=updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
list_frame = Frame(list_area, style="class:frame", title="Listes")

task_area = Window(content=updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
task_frame = Frame(task_area, style="class:frame", title="Tâches")


input_area = TextArea(multiline=False)
input_frame = Frame(input_area, style="class:frame")

layout = Layout(VSplit([Box(list_frame,padding=1,style="class:box"), Box(task_frame,padding=1,style="class:box")]))

show_input_frame = False
is_in_task_area = False
is_modifying = False

app = Application(key_bindings=kb, full_screen=True, style=style, layout=layout)

@kb.add("c-q")
def _(event):
    try :
        saveData()
    except:
        pass
    event.app.exit()

@kb.add("up")
def _(event):
    if not is_in_task_area:
        global selected_list
        if selected_list.id == 0:
            selected_list = all_list[len(all_list) - 1]
        else:
            selected_list = all_list[selected_list.id - 1]
        
        task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
        list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
    if is_in_task_area:
        global selected_task
        if selected_task.index == 0:
            selected_task = selected_list.tasks[len(selected_list.tasks) - 1]
        else:
            selected_task = selected_list.tasks[selected_task.index - 1]
        task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_task)

@kb.add("down")
def _(event):
    if not is_in_task_area:
        global selected_list
        if selected_list is not None and len(all_list) != 1:
            removeList(selected_list.id)
            if selected_list.id == len(all_list) - 1:
                selected_list = all_list[0]
            else:
                selected_list = all_list[selected_list.id + 1]
            if len(all_list) == 0: selected_list = None
        task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
        list_area.content = updateListArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list)
    
    if is_in_task_area:
        global selected_task
        if selected_task.index == len(selected_list.tasks) - 1:
            selected_task = selected_list.tasks[0]
        else:
            selected_task = selected_list.tasks[selected_task.index + 1]
        task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_task)

@kb.add("+")
def _(event):
    global show_input_frame
    layout = Layout(HSplit([VSplit([Box(list_frame, padding=1, style="class:box"), Box(task_frame, padding=1, style="class:box")]), Box(input_frame, padding=1, style="class:box")]))
    app.layout = layout
    app.layout.focus(input_area)
    show_input_frame = True

@kb.add("-")
def _(event):
    global is_in_task_area, selected_task, selected_list
    if not is_in_task_area:
        if selected_list is not None : removeList(selected_list.id) 
        if len(all_list) != 0:
            selected_list = all_list[selected_list.id - 1]
        if len(all_list) == 0: selected_list = None
        list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
        task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list)
    else:
        if len(selected_list.tasks) != 0: selected_list.removeTask(selected_task.index)
        if len(selected_list.tasks) == 0:
            is_in_task_area = False
            task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list)
        else:
            selected_task = selected_list.tasks[0]
            task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_task)

@kb.add("m") #modify name
def _(event):
    global show_input_frame, is_modifying
    if not show_input_frame:
        layout = Layout(HSplit([VSplit([Box(list_frame, padding=1, style="class:box"), Box(task_frame, padding=1, style="class:box")]), Box(input_frame, padding=1, style="class:box")]))
        app.layout = layout
        app.layout.focus(input_area)
        show_input_frame = True
        is_modifying = True

        
    


@kb.add("escape")
def _(event):
    global show_input_frame, is_in_task_area
    if show_input_frame:
        layout = Layout(HSplit([Box(list_frame, padding=1, style="class:box")]))
        app.layout = layout
        show_input_frame = False
    elif is_in_task_area:
        is_in_task_area = False
        task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)

@kb.add("enter")
def _(event):
    global show_input_frame, is_in_task_area, is_modifying, selected_task, selected_list
    if input_area.buffer.text.strip():
        if not is_in_task_area:
            if is_modifying:
                selected_list.name = input_area.text
                is_modifying = False
                saveSelectedList()
            else:
                addList(List(input_area.text, False, len(all_list), []))
                selected_list = all_list[len(all_list) - 1]
            input_area.text = ""
            list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
            layout = Layout(HSplit([VSplit([Box(list_frame, padding=1, style="class:box"), Box(task_frame, padding=1, style="class:box")])]))
            app.layout = layout
            show_input_frame = False
        else:
            if is_modifying:
                selected_task.name = input_area.text
                is_modifying = False
                saveSelectedTask()
            else:
                selected_list.addTask(input_area.text)
            input_area.text = ""
            task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_list.tasks[len(selected_list.tasks) - 1])
            layout = Layout(HSplit([VSplit([Box(list_frame, padding=1, style="class:box"), Box(task_frame, padding=1, style="class:box")])]))
            app.layout = layout
            show_input_frame = False
            try:
                selected_task = selected_list.tasks[len(selected_list.tasks) - 1]
            except:
                pass
            saveSelectedList()

    elif not is_in_task_area:
        is_in_task_area = True
        if selected_list.tasks: task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_list.tasks[0])
    elif is_in_task_area:
        try:
            selected_task.done = not selected_task.done
            task_area.content = updateTaskArea("class:task-done-unselected", "class:task-undone-unselected", "class:task-done-selected", "class:task-undone-selected", selected_list, selected_task)
            saveSelectedList()
        except:
            pass


if __name__ == "__main__":
    app.run()