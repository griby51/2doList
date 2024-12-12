from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, VSplit, Window, HSplit
from prompt_toolkit.widgets import Box, Frame, Label, TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import FormattedTextControl
import json

# Charger les données depuis le fichier JSON
with open("data.json", "r") as f:
    data = json.load(f)

# Styles pour l'application
style = Style.from_dict({
    "frame": "bg:#040404 fg:#106cbc",
    "box": "bg:#040404 fg:#106cbc",
    "list-undone-unselected": "bg:#040404 fg:#0b4583",
    "list-undone-selected": "bg:#106cbc fg:#05224b",
    "list-done-unselected": "bg:#040404 fg:#0b4583 strike",
    "list-done-selected": "bg:#106cbc fg:#05224b strike",
})

kb = KeyBindings()

class List:
    def __init__(self, name, done, id, tasks):
        self.name = name
        self.done = done
        self.id = id
        self.tasks = [self.Task(task["name"], task["done"]) for task in tasks]

    class Task:
        def __init__(self, name, done, index):
            self.name = name
            self.done = done

all_list = []
tasks_in_active_list = [] 

for list in data["lists"]:
    all_list.append(List(list["name"], list["done"], list["id"], list["tasks"]))



actual_selected_list_tasks = []

def updateListArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected=None):
    formatted_text = []

    for list in all_list:
        style = done_style if list.done else not_done_style
        if list.id == selected:
            style = selected_done_style if list.done else selected_not_done_style
        formatted_text.append((style, list.name + "\n"))  
    return FormattedTextControl(formatted_text)

def updateTask():
    global actual_selected_list_tasks
    actual_selected_list_tasks = []
    

def addList(new_list):
    all_list.append(new_list)

selected_list = None if len(all_list) == 0 else 0

list_area = Window(content=updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
list_frame = Frame(list_area, style="class:frame", title="Listes")

task_area = Window(content=updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
task_frame = Frame(task_area, style="class:frame", title="Tâches")


input_area = TextArea(multiline=False)
input_frame = Frame(input_area, style="class:frame")

layout = Layout(HSplit([Box(list_frame,padding=1,style="class:box"), Box(task_frame,padding=1,style="class:box")]))

show_input_frame = False

app = Application(key_bindings=kb, full_screen=True, style=style, layout=layout)

@kb.add("c-q")
def _(event):
    event.app.exit()

@kb.add("up")
def _(event):
    global selected_list
    selected_list = (selected_list - 1) % len(all_list)
    list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)

@kb.add("down")
def _(event):
    global selected_list
    selected_list = (selected_list + 1) % len(all_list)
    list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)

@kb.add("+")
def _(event):
    global show_input_frame
    layout = Layout(HSplit([Box(list_frame, padding=1, style="class:box"), Box(input_frame, padding=1, style="class:box")]))
    app.layout = layout
    app.layout.focus(input_area)
    show_input_frame = True

@kb.add("escape")
def _(event):
    global show_input_frame
    if show_input_frame:
        layout = Layout(HSplit([Box(list_frame, padding=1, style="class:box")]))
        app.layout = layout
        show_input_frame = False


@kb.add("enter")
def _(event):
    global show_input_frame
    if input_area.buffer.text.strip():
        addList(List(input_area.text, False, len(all_list), []))
        input_area.text = ""
        list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
        layout = Layout(HSplit([Box(list_frame, padding=1, style="class:box")]))
        app.layout = layout
        show_input_frame = False



if __name__ == "__main__":
    app.run()