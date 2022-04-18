
# IMPORTS
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

class Plot:

    def __init__(self):
        self.fig = plt.figure()
        self.ax = p3.Axes3D(self.fig)

    def animate_scatters(self, iteration, data, scatters):
        """
        Update the data held by the scatter plot and therefore animates it.
        Args:
            iteration (int): Current iteration of the animation
            data (list): List of the data positions at each iteration.
            scatters (list): List of all the scatters (One per element)
        Returns:
            list: List of scatters (One per element) with new coordinates
        """
        return self.ax.scatter(data[iteration][0], data[iteration][1], data[iteration][2], marker=m)

    def main(self, data):
        """
        Creates the 3D figure and animates it with the input data.
        Args:
            data (list): List of the data positions at each iteration.
            save (bool): Whether to save the recording of the animation. (Default to False).
        """

        # Attaching 3D axis to the figure

        # Initialize scatters
        scatters = data

        # Number of iterations
        iterations = len(data)

        # Setting the axes properties
        self.ax.set_xlim3d([-50, 50])
        self.ax.set_xlabel('X')

        self.ax.set_ylim3d([-50, 50])
        self.ax.set_ylabel('Y')

        self.ax.set_zlim3d([-50, 50])
        self.ax.set_zlabel('Z')

        self.ax.set_title('3D Animated Scatter Example')

        # Provide starting angle for the view.
        self.ax.view_init(25, 10)

        ani = animation.FuncAnimation(self.fig, self.animate_scatters, iterations, fargs=(data, scatters),
                                        interval=50, blit=False, repeat=True)

        plt.show()