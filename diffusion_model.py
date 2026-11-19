import numpy as np
import matplotlib.pyplot as plt  # pyplot is a sub section of matplotlib


def plot_profile(
    grid, elevation, color="r", title=None, output=None
):  # name the function "plot_profile"
    plt.figure()  # open figure window
    plt.plot(
        grid, elevation, color
    )  # plot x vs z in red - the initial profile, a cliff
    plt.xlabel("x")
    plt.ylabel("z")
    if title is not None:
        plt.title(title)
    if output is not None:
        plt.savefig(output)


def calculate_stable_time_step(grid_spacing, diffusivity):
    dx = grid_spacing
    D = diffusivity
    return 0.5 * dx**2 / D


if __name__ == "__main__":
    # Start by setting two fixed model parameters - the diffusivity and the size of the model domain. Best practice: Use descriptive variable names, don't just name the variable a single letter.

    D = 100  # diffusivity
    Lx = 300  # model domain

    # Next, we set up the grid using a NumPy array.

    dx = 0.5  # grid spacing between grid nodes
    x = np.arange(
        start=0, stop=Lx, step=dx
    )  # x is a numpy 1D array starting at zero, stopping at Lx, with spacing dx. arange is array range
    nx = len(x)  # number of grid nodes

    # Set the initial conditions for the model. The elvation $z$ is a step function with a high value to the left, a low value on the right, and a cliff in the middle of the domain.

    z = np.zeros_like(
        x
    )  # create elevation values - a numpy array of zeros with the same shape as x, so z is an array of 600 zeros with type "float"
    z_left = 500  # the left side of the domain is 500
    z_right = 0  # the right side of the domain is 0
    z[x <= Lx / 2] = (
        z_left  # create the step function: use subscript automation. for values of of z at x that are half of the domain size or less, set them to z_left
    )
    z[x > Lx / 2] = (
        z_right  # for values of z at x that are greater than half of the domain size, set them to z_right
    )

    # Plot the initial profile.
    plot_profile(x, z, title="Initial hillslope profile", output="initial_profile.png")

    # Set up time stepping for the model. Calculate a stable time step from a stability criterion.

    nt = 5000  # number of time steps
    dt = 0.5 * dx**2 / D  # time step size based on stability criterion for diffusion

    # Loop over the time steps of the model, solving the diffusion equation using the FTCS scheme described above.
    # Note the use of array operations on the elevation $z$.
    # The boundary conditions remain fixed in each time step.

    for t in range(0, nt):
        z[1:-1] += D * dt / dx**2 * (z[:-2] - 2 * z[1:-1] + z[2:])

    # Plot the result - we have diffused away the cliff.

    plot_profile(
        x, z, color="b", title="Final hillslope profile", output="final_profile.png"
    )
