import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def open_new_window():
    new_window = tk.Toplevel(root)
    label = tk.Label(new_window, text='HELLOOOO')
    label.pack()
    # new_fig = plt.figure()
    # new_canvas = FigureCanvasTkAgg(new_fig, master=new_window)
    # new_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


button = tk.Button(root, text='Open new window', command=open_new_window)
button.pack(side=tk.BOTTOM)

root.mainloop()
