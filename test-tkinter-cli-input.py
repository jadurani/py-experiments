from tkinter import *

ROOT = Tk()

def ask_for_userinput():
    user_input = input("Give me your command! Just type \"exit\" to close: ")
    if user_input == "exit":
        ROOT.quit()
    elif user_input == "destroy":
        ROOT.destroy()
    elif user_input == "hide":
        ROOT.withdraw()
    elif user_input == "show":
        ROOT.deiconify()
    else:
        label = Label(ROOT, text=user_input)
        label.pack()
    print(ROOT)
    ROOT.after(0, ask_for_userinput)


LABEL = Label(ROOT, text="Hello, world!")
LABEL.pack()
ROOT.after(0, ask_for_userinput)
ROOT.mainloop()