import tkinter as tk
import port_scanner_gui  # Import the port scanner module
import dos_attack_gui  # Import the DoS attack module


# Function to open the Port Scanner
def open_port_scanner():
    root.withdraw()  # Hide main menu
    port_scanner_gui.port_scanner_gui(root)  # Pass root to allow returning

# Function to open the DoS Attack Tool
def open_dos_attack():
    root.withdraw()  # Hide main menu
    dos_attack_gui.dos_attack_gui(root)  # Pass root to allow returning

# Create the main menu window
root = tk.Tk()
root.title("Penetration Testing Toolkit")
root.geometry("400x350")

tk.Label(root, text="Select a Tool:", font=("Arial", 14)).pack(pady=20)

# Buttons for each tool
tk.Button(root, text="Port Scanner", command=open_port_scanner, width=20, height=2).pack(pady=10)
tk.Button(root, text="DoS Attack", command=open_dos_attack, width=20, height=2).pack(pady=10)

# Exit Button
tk.Button(root, text="Exit", command=root.quit, width=20, height=2).pack(pady=20)

root.mainloop()
