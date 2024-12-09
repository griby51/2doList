from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, VSplit
from prompt_toolkit.widgets import Box, Frame, TextArea, Label
from prompt_toolkit.styles import Style
import json

with open("data.json", "r") as f:
    data = json.load(f)

style = Style.from_dict({
    "frame" : "bg:#040404 fg:#106cbc", 
    "box" : "bg:#040404 fg:#106cbc",
})

_list = data["lists"]

kb = KeyBindings()

list_area = TextArea(text="List area")
task_area = TextArea(text="Task area")

list_frame = Frame(title="Lists", body=list_area, style="class:frame")
task_frame = Frame(title="Tasks", body=task_area, style="class:frame")

layout = Layout(VSplit(
    [
        Box(list_frame, padding=1, style="class:box"),
        Box(task_frame, padding=1, style="class:box"),
    ]
))

app = Application(layout=layout, key_bindings=kb, full_screen=True, style=style)

#quit the application
@kb.add("c-q")
def _(event):
    event.app.exit()

if __name__ == "__main__":
    app.run()