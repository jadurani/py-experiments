import tkinter as tk
from tkinter import messagebox as mb

def threadDialog(intensity,pgd,pga): # thread for displaying alert box
  root = tk.Tk()
  root.withdraw()
  mb.showwarning('! EARTHQUAKE ALERT !', ('Intensity: %s\nDisplacement: %.2f m, '+'\nAcceleration: %.2f m/s2') % (intensity,pgd,pga))

threadDialog(1, 2, 3)