import tkinter as tk
from tkinter import ttk
import RPi.GPIO as GPIO
from smbus2 import SMBus
import time

# Initialize GPIO and DAC
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# DAC Address and Channels
dac_addr = 0x61  # Replace with your DAC address
dac_ch = [0, 8, 16, 24, 32, 40, 48, 56]
DAC_lat = 4
GPIO.setup(DAC_lat, GPIO.OUT)
DAC = SMBus(1)

# LED Control Functions
def set_dac_value(channel, value):
    """Set DAC value for a specific channel."""
    if value < 0 or value > 4095:
        raise ValueError("DAC value must be between 0 and 4095.")
    
    print(value)

    # Split the 12-bit value into two 8-bit bytes
    msb = (value >> 8) & 0xFF  # Most Significant Byte (upper 8 bits)
    lsb = value & 0xFF         # Least Significant Byte (lower 8 bits)

    # Send the data to the DAC
    GPIO.output(DAC_lat, GPIO.LOW)
    print(msb,lsb)
    DAC.write_i2c_block_data(dac_addr, dac_ch[channel], [msb, lsb])
    time.sleep(0.001)  # Small delay for stable communication
    GPIO.output(DAC_lat, GPIO.HIGH)

def update_leds():
    """Update all LEDs based on the input box values."""
    try:
        # Read values from input boxes
        red_value = int(red_entry.get())
        green_value = int(green_entry.get())
        blue_value = int(blue_entry.get())
        inner_value = int(inner_entry.get())
        outer_value = int(outer_entry.get())

        # Validate values
        if not (0 <= red_value <= 4095 and 0 <= green_value <= 4095 and
                0 <= blue_value <= 4095 and 0 <= inner_value <= 4095 and
                0 <= outer_value <= 4095):
            raise ValueError("Values must be between 0 and 4095.")

        # Set DAC values for each LED
        set_dac_value(6, red_value)    # Red LED (Channel 6)
        set_dac_value(4, green_value)  # Green LED (Channel 4)
        set_dac_value(2, blue_value)   # Blue LED (Channel 2)
        set_dac_value(5, inner_value)  # Inner LED (Channel 5)
        set_dac_value(7, outer_value)  # Outer LED (Channel 7)

        status_label.config(text="LEDs Updated Successfully!", fg="green")
    except ValueError as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")

# Create the GUI
root = tk.Tk()
root.title("Real-Time LED Control")
root.geometry("400x300")

# Input Boxes for DAC Values
ttk.Label(root, text="Red LED Value (0-4095):").grid(row=0, column=0, padx=10, pady=5)
red_entry = ttk.Entry(root)
red_entry.grid(row=0, column=1, padx=10, pady=5)
red_entry.insert(0, "0")

ttk.Label(root, text="Green LED Value (0-4095):").grid(row=1, column=0, padx=10, pady=5)
green_entry = ttk.Entry(root)
green_entry.grid(row=1, column=1, padx=10, pady=5)
green_entry.insert(0, "0")

ttk.Label(root, text="Blue LED Value (0-4095):").grid(row=2, column=0, padx=10, pady=5)
blue_entry = ttk.Entry(root)
blue_entry.grid(row=2, column=1, padx=10, pady=5)
blue_entry.insert(0, "0")

ttk.Label(root, text="Inner LED Value (0-4095):").grid(row=3, column=0, padx=10, pady=5)
inner_entry = ttk.Entry(root)
inner_entry.grid(row=3, column=1, padx=10, pady=5)
inner_entry.insert(0, "0")

ttk.Label(root, text="Outer LED Value (0-4095):").grid(row=4, column=0, padx=10, pady=5)
outer_entry = ttk.Entry(root)
outer_entry.grid(row=4, column=1, padx=10, pady=5)
outer_entry.insert(0, "0")

# Update Button
update_button = ttk.Button(root, text="Update LEDs", command=update_leds)
update_button.grid(row=5, column=0, columnspan=2, pady=10)

# Status Label
status_label = ttk.Label(root, text="", font=("Arial", 10))
status_label.grid(row=6, column=0, columnspan=2)

# Run the GUI
root.mainloop()

# Cleanup GPIO on exit
GPIO.cleanup()