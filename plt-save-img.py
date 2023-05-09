import matplotlib.pyplot as plt

# create a figure and plot something
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [1, 4, 2, 3])

# save the figure as a PNG image
fig.savefig('my_plot.png')
