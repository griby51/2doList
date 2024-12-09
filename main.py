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
    "task-done": "fg:#00ff00",  # Vert pour les tâches terminées
    "task-not-done": "fg:#ff0000",  # Rouge pour les tâches non terminées
    "list-done": "strike",
    "selected-list" : "bg:#106cbc fg:#040404",
    "normal-list" : "bg:#040404 fg:#106cbc",
})

selectedList = 1

allList = data["lists"]

kb = KeyBindings()

def updateList(lists):
    formatted_text = []
    
    for i in lists:
        if i["id"] == selectedList:
            formatted_text.append(("class:selected-list", i["name"] + "\n"))
        else:
            formatted_text.append(("class:normal-list", i["name"] + "\n"))

    return FormattedTextControl(formatted_text)

# Générer le contenu de la liste de tâches formaté
def updateTaskIfDone(task):
    formatted_text = []
    
    for i in task:
        color = "class:task-done" if i["done"] else "class:task-not-done"
        formatted_text.append((color, i["name"] + "\n"))
    return FormattedTextControl(formatted_text)


# Créer les zones de texte
list_area = Window(content=updateList(allList))

task_area = Window(content=updateTaskIfDone(allList[selectedList]["tasks"]))

# Encadrer les zones de texte
list_frame = Frame(title="Lists", body=list_area, style="class:frame")
task_frame = Frame(title="Tasks", body=task_area, style="class:frame")

input_area = TextArea(prompt="", height=1, style="class:input")
input_frame = Frame(title="Input", style="class:frame", body=input_area)

# Mise en page
layout = Layout(VSplit(
    [
        HSplit([
            Box(list_frame, padding=1, style="class:box"),
            Box(input_frame, padding=1, style="class:box"),
        ]),

        Box(task_frame, padding=1, style="class:box"),
    ]
))

# Application
app = Application(layout=layout, key_bindings=kb, full_screen=True, style=style)

# Quitter l'application
@kb.add("c-q")
def _(event):
    event.app.exit()

@kb.add("up")
def _(event):
    global selectedList
    if selectedList == 0:
        selectedList = len(allList) - 1
    else:
        selectedList -= 1

    list_area.content = updateList(allList)
    task_area.content = updateTaskIfDone(allList[selectedList]["tasks"])

@kb.add("down")
def _(event):
    global selectedList
    if selectedList == len(allList) - 1:
        selectedList = 0
    else:
        selectedList += 1

    list_area.content = updateList(allList)
    task_area.content = updateTaskIfDone(allList[selectedList]["tasks"])

if __name__ == "__main__":
    app.run()
