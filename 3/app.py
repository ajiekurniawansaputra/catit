import tkinter as tk

def handle_click(event):
    if button["text"] == "Start":
        button["text"] = "Stop"
        button["bg"]="Red"
    else:
        button["text"] ="Start"
        button["bg"]="Black",

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