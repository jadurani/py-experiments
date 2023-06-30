
def clean_up_axis(ax):
	'''
	Sets up the axes such that it will look like a plain rectangle.
	'''
	ax.xaxis.set_tick_params(labelbottom=False)
	ax.yaxis.set_tick_params(labelleft=False)

	# Hide X and Y axes tick marks
	ax.set_xticks([])
	ax.set_yticks([])

	# hide spines
	ax.spines['top'].set_visible(False)
	ax.spines['right'].set_visible(False)
	ax.spines['left'].set_visible(False)
	ax.spines['bottom'].set_visible(False)
