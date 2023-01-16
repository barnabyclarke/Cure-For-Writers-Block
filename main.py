import math
from tkinter import *
from tkinter import ttk

BACKGROUND_COLOUR = "#1B4F72"
WORD_LIST = (150, 250, 350, 500, 750, 1000, 2000)
TIME_LIST = (3, 5, 7, 10, 15, 20, 25)
TIMER = ""
TYPE_TIMER = ""


def restart():
    window.after_cancel(TIMER)
    window.after_cancel(TYPE_TIMER)
    text_box.grid_forget()
    restart_button.grid_forget()
    scroll.grid_forget()
    canvas.itemconfig(timer_text, text="")

    start_screen()


def start_screen():
    canvas.itemconfig(title, text="The Cure for Writers Block")
    canvas.itemconfig(instructions, text="All your text will clear if you dont type in 5 seconds")
    canvas.grid(column=0, row=0, columnspan=5)
    word_radbut.grid(column=1, row=2, sticky=E)
    word_radbut.invoke()
    time_radbut.grid(column=1, row=3, sticky=E)
    list_box.grid(column=2, row=2, rowspan=2)
    list_box.selection_set(first=0)
    start_button.grid(column=2, row=4, pady=35, sticky=W)


def list_values(radio_choice):
    if radio_choice["text"] == "Word goal":
        return list_box.config(listvariable=word_list_choice)
    if radio_choice["text"] == "Time limit\n(mins)":
        return list_box.config(listvariable=time_list_choice)


def start(*args):
    list_box.grid_forget()
    start_button.grid_forget()
    word_radbut.grid_forget()
    time_radbut.grid_forget()
    canvas.itemconfig(title, text="Begin typing")

    value = int(list_box.curselection()[0])
    if radbut_choice.get() == "word":
        choice = WORD_LIST[value]
    else:
        choice = TIME_LIST[value]

    # Word counter - TODO
    if choice > 25:
        canvas.itemconfig(instructions, text="Counting words")

    # Timer
    else:
        canvas.itemconfig(instructions, text="Counting time")
        counter(choice * 60)

    text_box.grid(column=1, row=2, columnspan=3, sticky=W)
    scroll.grid(column=4, row=2, sticky=N + S + W)
    restart_button.grid(column=1, row=4, pady=35, sticky=W)


def key_input(event=None):
    global TYPE_TIMER
    if TYPE_TIMER != "":
        window.after_cancel(TYPE_TIMER)
        TYPE_TIMER = ""
    type_counter(5)


def type_counter(count):
    global TYPE_TIMER
    if int(count) > 0:
        TYPE_TIMER = window.after(1000, type_counter, count - 1)
    else:
        text_box.delete("1.0", END)


def counter(count):
    global TIMER
    if radbut_choice.get() == 'time':
        count_min = math.floor(count / 60)
        count_sec = count % 60
        if count_sec < 10:
            count_sec = f"0{count_sec}"
        if count > 0:
            canvas.itemconfig(timer_text, text=f'Time: {count_min}:{count_sec}')
            TIMER = window.after(1000, counter, count - 1)
        else:
            canvas.itemconfig(title, text='Well done!')


window = Tk()

radbut_choice = StringVar()
word_list_choice = StringVar(value=WORD_LIST)
time_list_choice = StringVar(value=TIME_LIST)

window.title("Cure for Writers Block")
window.minsize()
window.config(padx=20, pady=20, bg=BACKGROUND_COLOUR)

# # --- TEXT --- # #
canvas = Canvas(width=800, height=300, highlightthickness=0, bg=BACKGROUND_COLOUR)
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="white")
instructions = canvas.create_text(400, 210, text="", font=("Ariel", 15, "italic"), fill="grey")
timer_text = canvas.create_text(700, 20, text="", font=("Ariel", 15, "italic"), fill="grey")

# # --- INTERACTIVES --- # #
# Radio
word_radbut = ttk.Radiobutton(text="Word goal", variable=radbut_choice, value="word",
                              command=lambda: list_values(word_radbut))
time_radbut = ttk.Radiobutton(text="Time limit\n(mins)", variable=radbut_choice, value="time",
                              command=lambda: list_values(time_radbut))

# Listbox
list_box = Listbox(height=7, activestyle="none")

# Buttons
start_button = Button(text="Begin Test", font=('Ariel', 20, 'bold'), background="white", command=start)
restart_button = Button(text="Restart", font=('Ariel', 10, 'bold'), background="white", command=restart)

# Textbox
scroll = Scrollbar()
text_box = Text(borderwidth=0, background=BACKGROUND_COLOUR, relief="flat", wrap="word", font=("Ariel", 15, "normal"),
                width=70, height=15, fg="white", insertbackground="white", yscrollcommand=scroll.set)
text_box.bind("<Key>", key_input)
scroll.config(command=text_box.yview)

start_screen()
window.mainloop()
