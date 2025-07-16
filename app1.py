import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from PIL import Image, ImageTk

def predict_failure_for_all_types():
    try:
        rotational_speed = int(rotational_speed_entry.get())
        torque = float(torque_entry.get())
        tool_wear = int(tool_wear_entry.get())
        temp_difference = float(temp_difference_entry.get())

        power = torque * rotational_speed * 0.104719755
        strain = torque * tool_wear

        # Pass input values to the simulation
        machine_failure_simulation.input['air_temperature'] = 298.2  # Sample value
        machine_failure_simulation.input['process_temperature'] = 308.7  # Sample value
        machine_failure_simulation.input['rotational_speed'] = rotational_speed
        machine_failure_simulation.input['torque'] = torque
        machine_failure_simulation.input['tool_wear'] = tool_wear

        # Compute the output
        machine_failure_simulation.compute()

        # Print the predicted machine failure
        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, f"Predicted Machine Failure: {machine_failure_simulation.output['machine_failure']}\n")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def visualize_fuzzy():
    air_temperature.view()
    process_temperature.view()
    rotational_speed.view()
    torque.view()
    tool_wear.view()
    machine_failure.view()

# Create a Tkinter window
root = tk.Tk()
root.title("Predict Failure for All Types")
root.geometry("739x416")

# Load background image
background_image = Image.open("bg7.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create input fields
input_frame = ttk.Frame(root, style="Input.TFrame")
input_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.4)

rotational_speed_label = ttk.Label(input_frame, text="Rotational Speed [rpm]:")
rotational_speed_label.grid(row=0, column=0, padx=5, pady=5)
rotational_speed_entry = ttk.Entry(input_frame)
rotational_speed_entry.grid(row=0, column=1, padx=5, pady=5)

torque_label = ttk.Label(input_frame, text="Torque [Nm]:")
torque_label.grid(row=1, column=0, padx=5, pady=5)
torque_entry = ttk.Entry(input_frame)
torque_entry.grid(row=1, column=1, padx=5, pady=5)

tool_wear_label = ttk.Label(input_frame, text="Tool Wear [min]:")
tool_wear_label.grid(row=2, column=0, padx=5, pady=5)
tool_wear_entry = ttk.Entry(input_frame)
tool_wear_entry.grid(row=2, column=1, padx=5, pady=5)

temp_difference_label = ttk.Label(input_frame, text="Temperature Difference [k]:")
temp_difference_label.grid(row=3, column=0, padx=5, pady=5)
temp_difference_entry = ttk.Entry(input_frame)
temp_difference_entry.grid(row=3, column=1, padx=5, pady=5)

# Create results frame
results_frame = ttk.Frame(root, style="Input.TFrame")
results_frame.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.3)

results_label = ttk.Label(results_frame, text="Results:", font=("Helvetica", 12))
results_label.place(relx=0.1, rely=0.1)

results_text = tk.Text(results_frame, height=2, width=50)
results_text.place(relx=0.1, rely=0.4)

# Define fuzzy variables
air_temperature = ctrl.Antecedent(np.arange(298, 299, 0.1), 'air_temperature')
process_temperature = ctrl.Antecedent(np.arange(308, 309, 0.1), 'process_temperature')
rotational_speed = ctrl.Antecedent(np.arange(1400, 1600, 1), 'rotational_speed')
torque = ctrl.Antecedent(np.arange(39, 50, 0.1), 'torque')
tool_wear = ctrl.Antecedent(np.arange(0, 11, 1), 'tool_wear')
machine_failure = ctrl.Consequent(np.arange(0, 2, 1), 'machine_failure')

# Define membership functions
# Air temperature
air_temperature['low'] = fuzz.trimf(air_temperature.universe, [298, 298, 298.5])
air_temperature['high'] = fuzz.trimf(air_temperature.universe, [298.4, 298.9, 299])

# Process temperature
process_temperature['low'] = fuzz.trimf(process_temperature.universe, [308, 308, 308.5])
process_temperature['high'] = fuzz.trimf(process_temperature.universe, [308.4, 308.9, 309])

# Rotational speed
rotational_speed['low'] = fuzz.trimf(rotational_speed.universe, [1400, 1400, 1500])
rotational_speed['high'] = fuzz.trimf(rotational_speed.universe, [1450, 1550, 1600])

# Torque
torque['low'] = fuzz.trimf(torque.universe, [39, 39, 44])
torque['high'] = fuzz.trimf(torque.universe, [42, 47, 50])

# Tool wear
tool_wear['low'] = fuzz.trimf(tool_wear.universe, [0, 0, 5])
tool_wear['high'] = fuzz.trimf(tool_wear.universe, [3, 8, 10])

# Machine failure
machine_failure['no'] = fuzz.trimf(machine_failure.universe, [0, 0, 1])
machine_failure['yes'] = fuzz.trimf(machine_failure.universe, [0, 1, 1])

# Define rules
rule1 = ctrl.Rule(air_temperature['low'] | process_temperature['low'] | rotational_speed['low'] | torque['low'] | tool_wear['high'], machine_failure['yes'])
rule2 = ctrl.Rule(air_temperature['high'] | process_temperature['high'] | rotational_speed['high'] | torque['high'] | tool_wear['low'], machine_failure['no'])

# Create control system
machine_failure_ctrl = ctrl.ControlSystem([rule1, rule2])
machine_failure_simulation = ctrl.ControlSystemSimulation(machine_failure_ctrl)

# Button to trigger prediction
predict_button = ttk.Button(root, text="Predict", command=predict_failure_for_all_types)
predict_button.place(relx=0.2, rely=0.9, relwidth=0.2, relheight=0.05)

# Button to visualize fuzzy system
visualize_button = ttk.Button(root, text="Visualize Fuzzy", command=visualize_fuzzy)
visualize_button.place(relx=0.6, rely=0.9, relwidth=0.2, relheight=0.05)

# Run the GUI event loop
root.mainloop()
