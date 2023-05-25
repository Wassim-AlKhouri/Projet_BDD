import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Replace this with your actual 4x4 quadrant data
quadrant_data = np.array([
    [210,291,362,443],
    [312,511,847,913],
    [411,921,1496,1664],
    [473,1032,1851,2046]]
)

# Create a grid for the x and y data
x = np.linspace(0, 4, 4)
y = np.linspace(0, 4, 4)
x_grid, y_grid = np.meshgrid(x, y)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the 3D graph using the x, y, and quadrant data
ax.plot_surface(x_grid, y_grid, quadrant_data, cmap='viridis')

# Set axis labels
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Light Intensity')

# Show the plot
plt.show()
