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
        self.tasks = tasks

    class Task:
        def __init__(self, name, done):
            self.name = name
            self.done = done

all_list = []

for list in data["lists"]:
    all_list.append(List(list["name"], list["done"], list["id"], list["tasks"]))

def updateListArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected=None):
    formatted_text = []

    for list in all_list:
        style = done_style if list.done else not_done_style
        if list.id == selected:
            style = selected_done_style if list.done else selected_not_done_style
        formatted_text.append((style, list.name + "\n"))  
    return FormattedTextControl(formatted_text)

def addList(new_list):
    all_list.append(new_list)

selected_list = None if len(all_list) == 0 else 0

list_area = Window(content=updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
list_frame = Frame(list_area, style="class:frame", title="Listes")

input_area = TextArea(multiline=False)
input_frame = Frame(input_area, style="class:frame", height=1)

show_input_frame = False


layout = Layout(HSplit([Box(list_frame,padding=1,style="class:box"),
                        Box(input_frame,padding=1,style="class:box")
                        ]))


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

if __name__ == "__main__":
    app.run()