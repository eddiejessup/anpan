import numpy as np
import scipy.ndimage.filters as ft
import matplotlib.pyplot as pp
import matplotlib.colors as cl

# Dimensionality of the system
d = 2
# Array size
M = 400
# Wave propagation speed
l = 0.08
# Run-time
t = 10000
# How often to update the plot
every = 20
# How often to add a raindrop (rate is a bad name, larger actually means less often)
rate = 40

# Set up a figure window with an array color plot 'im', using a logarithmic color scale
fig = pp.figure()
ax = fig.gca()
ax.set_xticks([])
ax.set_yticks([])
im = ax.imshow([[1]], norm=cl.LogNorm())

# Set up a 3xMxM array to hold the state of the system at the current, last and last-but-one timesteps
a = np.ones([3] + d * [M])

for i in range(t):
    # Iterate the system according the finite-difference algorithm
    a[0] = 2.0 * a[1] - a[2] + l * ft.laplace(a[1])

    # Every 'rate' iterations, add 1.0 to a random array index
    if i % rate == 0:
        a[0][tuple(np.random.randint(0, M, size=d))] += 1.0
        # Subtract a bit from all of the array to keep the overall sum constant
        a[0] -= 1.0 / a[0].size

    # Every 'every' iterations, update the plot and save an image
    if i % every == 0:
        im.set_data(a[0])
        fig.savefig('%08i.png' % i)
        print('%.2f%%' % (100.0 * float(i) / t))
        # Hack to make the colormap scaling work correctly
        if i == 0:
            im.autoscale()

    # Shift the last array into last-but-one, and current into last
    a[2] = a[1]
    a[1] = a[0]
