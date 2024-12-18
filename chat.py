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
        self.tasks = [self.Task(i, task["name"], task["done"]) for i, task in enumerate(tasks)]  # Charger les tâches

    class Task:
        def __init__(self, id, name, done):
            self.id = id  # Index unique
            self.name = name
            self.done = done

    def add_task(self, task_name):
        """Ajouter une tâche avec un nouvel index unique."""
        new_id = len(self.tasks)  # Index basé sur la longueur actuelle des tâches
        self.tasks.append(self.Task(new_id, task_name, False))

    def remove_task(self, task_id):
        """Supprimer une tâche par son ID."""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._reindex_tasks()

    def toggle_task_done(self, task_id):
        """Basculer l'état 'fait' d'une tâche."""
        for task in self.tasks:
            if task.id == task_id:
                task.done = not task.done
                break

    def _reindex_tasks(self):
        """Réattribuer les IDs pour garantir la continuité des index."""
        for i, task in enumerate(self.tasks):
            task.id = i

all_list = []

for list_data in data["lists"]:
    all_list.append(List(list_data["name"], list_data["done"], list_data["id"], list_data["tasks"]))

def updateListArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected=None):
    formatted_text = []

    for lst in all_list:
        style = done_style if lst.done else not_done_style
        if lst.id == selected:
            style = selected_done_style if lst.done else selected_not_done_style
        formatted_text.append((style, lst.name + "\n"))
    return FormattedTextControl(formatted_text)

def updateTaskArea(done_style, not_done_style, selected_done_style, selected_not_done_style, selected_list):
    if selected_list is None or selected_list >= len(all_list):
        return FormattedTextControl([])  # Pas de liste sélectionnée

    formatted_text = []
    active_list = all_list[selected_list]

    for task in active_list.tasks:
        style = done_style if task.done else not_done_style
        formatted_text.append((style, f"[{task.id}] {task.name}\n"))  # Afficher l'index

    return FormattedTextControl(formatted_text)

def addList(new_list):
    all_list.append(new_list)

selected_list = None if len(all_list) == 0 else 0

list_area = Window(content=updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
list_frame = Frame(list_area, style="class:frame", title="Listes")

task_area = Window(content=updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list))
task_frame = Frame(task_area, style="class:frame", title="Tâches")

input_area = TextArea(multiline=False)
input_frame = Frame(input_area, style="class:frame")

layout = Layout(VSplit([
    Box(list_frame, padding=1, style="class:box"),
    Box(task_frame, padding=1, style="class:box")
]))

show_input_frame = False

app = Application(key_bindings=kb, full_screen=True, style=style, layout=layout)

@kb.add("c-q")
def _(event):
    event.app.exit()

@kb.add("up")
def _(event):
    global selected_list, task_area
    selected_list = (selected_list - 1) % len(all_list)
    list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
    task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)

@kb.add("down")
def _(event):
    global selected_list, task_area
    selected_list = (selected_list + 1) % len(all_list)
    list_area.content = updateListArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
    task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)

@kb.add("+")
def _(event):
    global show_input_frame
    layout = Layout(HSplit([
        Box(list_frame, padding=1, style="class:box"),
        Box(task_frame, padding=1, style="class:box"),
        Box(input_frame, padding=1, style="class:box")
    ]))
    app.layout = layout
    app.layout.focus(input_area)
    show_input_frame = True

@kb.add("escape")
def _(event):
    global show_input_frame
    if show_input_frame:
        layout = Layout(HSplit([
            Box(list_frame, padding=1, style="class:box"),
            Box(task_frame, padding=1, style="class:box")
        ]))
        app.layout = layout
        show_input_frame = False

@kb.add("enter")
def _(event):
    global show_input_frame
    if input_area.buffer.text.strip():
        if show_input_frame:
            addList(List(input_area.text, False, len(all_list), []))
        else:
            if selected_list is not None:
                all_list[selected_list].add_task(input_area.text.strip())
                task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
        input_area.text = ""
        layout = Layout(HSplit([
            Box(list_frame, padding=1, style="class:box"),
            Box(task_frame, padding=1, style="class:box")
        ]))
        app.layout = layout
        show_input_frame = False

@kb.add("t")
def toggle_task(event):
    global selected_list, input_area, task_area

    if selected_list is None:
        print("Aucune liste sélectionnée !")
        return

    # Vérifiez si un ID de tâche est entré
    if input_area.buffer.text.strip().isdigit():
        task_id = int(input_area.buffer.text.strip())
        all_list[selected_list].toggle_task_done(task_id)
        input_area.buffer.text = ""  # Réinitialiser l'input
        task_area.content = updateTaskArea("class:list-done-unselected", "class:list-undone-unselected", "class:list-done-selected", "class:list-undone-selected", selected_list)
    else:
        print("Veuillez entrer un ID valide pour basculer l'état d'une tâche.")

if __name__ == "__main__":
    app.run()
