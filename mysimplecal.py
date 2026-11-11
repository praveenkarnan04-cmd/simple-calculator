import tkinter as tk
import re

reset_display = False   #keep adding numbers on display and true will clear the display before add a num
last_operator = ""
last_number = ""


cal = tk.Tk()                #creat a window
cal.title("Simple Calculator")
cal.geometry("370x530")
cal.resizable(False, False)
cal.configure(bg="#f0f0f0")

# entry
entry = tk.Entry(
    cal,
    bd=0,
    bg="#f0f0f0",
    fg="black",
    font=('arial', 40),
    justify='right',
    width=20
)
entry.pack(ipady=30, ipadx=10, padx=10, pady=10, fill="both")
entry.insert(0, "0")    #for default zero
entry.focus_set()

# cursor blink
entry.config(insertontime=500, insertofftime=500)


# ---------- FUNCTIONS ----------

def press_enter(event):
    click("=")          #this will call the click (button_text function

#key board handling part
def press_key(event):
    key = event.char
    sym = event.keysym

    if key.isdigit():
        click(key)
    elif key in "+-*/.%()":
        click(key)
    elif sym == "Return":    # pressing enter works like "="
        click("=")
    elif sym == "BackSpace":
        click("⌫")

    return "break"  # this will stop twice typing 


entry.bind("<Return>", press_enter)
entry.bind("<KP_Enter>", press_enter)
entry.bind("<Key>", press_key)


def click(button_text):
    global reset_display, last_operator, last_number

    text = entry.get()

    # limit input length
    if len(text) >= 12 and button_text not in ["C", "⌫", "="]:
        return

    # CLEAR
    if button_text == "C":
        entry.delete(0, tk.END)
        entry.insert(0, "0")
        reset_display = False
        return

    # BACKSPACE
    elif button_text == "⌫":
        if text != "0":
            text = text[:-1]
            if text == "":
                text = "0"

            entry.delete(0, tk.END)
            entry.insert(0, text)
        return

    # SQUARE
    elif button_text == "X²":
        try:
            result = str(float(text) ** 2)
            entry.delete(0, tk.END)
            entry.insert(0, result[:12])    #result[ :12] this will limit the entry digits
        except:
            entry.delete(0, tk.END)
            entry.insert(0, "Error")
        return

    # EQUAL
    elif button_text == "=":
        try:
            expression = entry.get().replace('%', '/100').replace('X', '*')
            expression = re.sub(r'(\d)\(', r'\1*(', expression)

            # store last operation
            match = re.search(r'([+\-*/])(\d+\.?\d*)$', expression) #r'' (raw string)
                                                                          #Tells Python to treat backslashes \ normall   \d+ → one or more digits (2, 45, 100)
                                                                         #\.? → optional decimal point (. may or may not exist)
                                                                         #\d* → digits after decimal (5.2, 3.14)
            if match:
                last_operator = match.group(1)
                last_number = match.group(2)
            elif last_operator and last_number:
                expression = entry.get() + last_operator + last_number

            result = eval(expression)

            entry.delete(0, tk.END)
            entry.insert(0, str(result))

            reset_display = True

        except Exception:
            entry.delete(0, tk.END)
            entry.insert(0, "Error")
            reset_display = True

        return

    # NORMAL INPUT
    else:
        if reset_display:
            entry.delete(0, tk.END)
            reset_display = False

        if entry.get() == "0":
            entry.delete(0, tk.END)

        entry.insert(tk.END, button_text)


# ---------- BUTTON FRAME ----------

btnframe = tk.Frame(cal, bg="#f0f0f0")
btnframe.pack(padx=8, pady=8)


buttons = [
    ['C', 'X²', '⌫', '/'],
    ['7', '8', '9', '*'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['(', '0', ')', '='],
]

for i in range(len(buttons)):
    for j in range(len(buttons[i])):
        text = buttons[i][j]

        bg_color = "#f0f0f0"
        fg_color = "marron"

        if text == "C":
            bg_color = "orange"
            fg_color = "white"
        elif text in ("*", "/", "+", "-", "X²", "⌫"):
            bg_color = "white"
            fg_color = "red"
        elif text == "=":
            bg_color = "orange"
            fg_color = "white"

        btn = tk.Button(
            btnframe,
            text=text,
            font=('Arial', 13),
            width=6,
            height=2,
            bd=5,
            bg=bg_color,
            fg=fg_color,
            command=lambda t=text: click(t)
        )

        btn.grid(row=i, column=j, padx=7, pady=7)


cal.mainloop()