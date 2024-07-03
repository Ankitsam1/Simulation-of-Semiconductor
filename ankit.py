import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_simulation():
    # Get input values from the GUI
    D = float(diffusion_coefficient.get())
    t = float(simulation_time.get()) * 3600  # Convert hours to seconds
    L = float(semiconductor_length.get())
    Nx = int(grid_points.get())

    # Discretize space
    x = np.linspace(0, L, Nx)
    dx = x[1] - x[0]

    # Initial concentration
    C = np.zeros(Nx)
    C[Nx // 2] = 1  # Impurity initially at the center

    # Time-stepping parameters
    dt = 0.9 * dx ** 2 / (2 * D)  # Stability condition
    Nt = int(t / dt)

    # Simulation loop
    for n in range(Nt):
        C_new = C.copy()
        for i in range(1, Nx - 1):
            C_new[i] = C[i] + D * dt / dx ** 2 * (C[i + 1] - 2 * C[i] + C[i - 1])
        C = C_new

    # Plot the results
    fig, ax = plt.subplots()
    ax.plot(x, C, label=f't = {simulation_time.get()} hour(s)')
    ax.set_xlabel('Position (cm)')
    ax.set_ylabel('Concentration')
    ax.set_title('Diffusion of Impurities in Semiconductor')
    ax.legend()

    # Display the plot in the GUI
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, columnspan=2)

# Create the main window
root = tk.Tk()
root.title("Semiconductor Diffusion Simulation")

# Create and place widgets
ttk.Label(root, text="Diffusion Coefficient (cm^2/s):").grid(row=0, column=0, sticky=tk.W)
diffusion_coefficient = ttk.Entry(root)
diffusion_coefficient.grid(row=0, column=1)

ttk.Label(root, text="Simulation Time (hours):").grid(row=1, column=0, sticky=tk.W)
simulation_time = ttk.Entry(root)
simulation_time.grid(row=1, column=1)

ttk.Label(root, text="Semiconductor Length (cm):").grid(row=2, column=0, sticky=tk.W)
semiconductor_length = ttk.Entry(root)
semiconductor_length.grid(row=2, column=1)

ttk.Label(root, text="Grid Points:").grid(row=3, column=0, sticky=tk.W)
grid_points = ttk.Entry(root)
grid_points.grid(row=3, column=1)

ttk.Button(root, text="Run Simulation", command=run_simulation).grid(row=4, columnspan=2)

# Create a frame to hold the plot
frame = ttk.Frame(root)
frame.grid(row=5, columnspan=2)

# Start the main event loop
root.mainloop()
