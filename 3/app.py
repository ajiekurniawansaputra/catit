import tkinter as tk
from numpy import random

class state:
    def __init__(self):
        self.sensor = False

def sensor1_simulation():
    try:
        if app_state.sensor==True:
            print("sensor 1: ",random.rand())
            window.after(2000,sensor1_simulation)
    except:
        raise "error"

def sensor2_simulation():
    try:
        if app_state.sensor==True:
            print("sensor 2: ",random.rand())
            window.after(2000,sensor2_simulation)
    except:
        raise "error"

def handle_click(event):
    if button["text"] == "Start":
        app_state.sensor = True
        window.after(0,sensor1_simulation)
        window.after(0,sensor2_simulation)
        button["text"] = "Stop"
        button["bg"]="Red"
    else:
        app_state.sensor = False
        button["text"] ="Start"
        button["bg"]="Black",

app_state = state()

window = tk.Tk()
button = tk.Button(
    text="Start",
    width=15,
    height=3,
    bg="Black",
    fg="White",
)
button.bind("<Button-1>", handle_click)
button.pack()
window.mainloop()