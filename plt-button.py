import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import use, rcParams

rcParams['toolbar'] = 'None'
use('Qt5Agg')
plt.ion()

def on_button_clicked(event):
    # Perform the desired action when the button is clicked
    print("Button clicked!")


fig, ax = plt.subplots()

# Create the button and position it within the figure
button_ax = plt.axes([0.7, 0.7, 0.2, 0.1])
button = Button(button_ax, "Click Me")

# Connect the button click event to the function
button.on_clicked(on_button_clicked)

fig.canvas.start_event_loop(5)
