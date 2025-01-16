import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import backend

# --- Set Theme ---
root = tk.Tk()
root.title("Posture Monitor")
root.geometry("500x400")
root.option_add("*tearOff", False)

# Configure grid layout for centering
root.columnconfigure(0, weight=1)  # Center widgets in the column
root.rowconfigure([0, 1, 2], weight=1)  # Equal weight to rows

# Apply the Forest theme
style = ttk.Style(root)
root.tk.call('source', './theme/forest-dark.tcl')
style.theme_use('forest-dark')

# Title label centered
title_label = ttk.Label(root, text="Posture Monitor", font=("Arial", 24), anchor="center", justify="center")
title_label.grid(row=0, column=0, pady=10, sticky="nsew")  # Use "nsew" for full centering

# Separator below the title
separator = ttk.Separator(root)
separator.grid(row=1, column=0, pady=10, sticky="ew")

# Adjust column weight for centering
root.grid_columnconfigure(0, weight=1)

# --- Global Variables ---
baseline = None
running = False
ser = None
posture_message_label = tk.Label(root, text="Checking connection...", font=("Arial", 16), fg="white", width=50, height=4)
timer_label = None

# --- Main Window ---
def main_window():
    """Main window with Start, Information, Exit buttons."""
    global posture_message_label
    for widget in root.winfo_children():
        widget.grid_forget()  # Clear the window

    title_label.grid(row=0, column=0, pady=10, sticky="ew")
    separator.grid(row=1, column=0, pady=10, sticky="ew")
    posture_message_label.grid(row=2, column=0, pady=20)

    btn_start = ttk.Button(root, text="Start Session", style="Accent.TButton", command=start_calibration)
    btn_start.grid(row=3, column=0, pady=10)

    btn_information = ttk.Button(root, text="Information", command=information_window)
    btn_information.grid(row=4, column=0, pady=10)

    btn_exit = ttk.Button(root, text="Exit", command=exit_app)
    btn_exit.grid(row=5, column=0, pady=10)

# --- Calibration Timer ---
def start_calibration():
    """Start calibration and transition to posture monitoring."""
    for widget in root.winfo_children():
        widget.grid_forget()

    countdown_label = tk.Label(root, text="Calibrating... Hold your posture!", font=("Arial", 16), fg="white")
    countdown_label.grid(row=2, column=0, pady=20)

    def update_countdown(remaining):
        if remaining > 0:
            countdown_label.config(text=f"Calibrating... Hold still for {remaining} seconds.")
            root.after(1000, update_countdown, remaining - 1)
        else:
            perform_calibration()

    update_countdown(5)

def perform_calibration():
    """Perform calibration and move to posture monitoring."""
    global baseline
    values = []
    start_time = time.time()
    while time.time() - start_time < 3:
        value = backend.read_flex_value(ser)
        if value is not None:
            values.append(value)

    if values:
        baseline = sum(values) // len(values)
        messagebox.showinfo("Calibration", "Calibration complete!")
        posture_monitor_window()
    else:
        messagebox.showerror("Calibration", "Calibration failed. Please try again!")
        main_window()

# --- Posture Monitoring Window ---
def posture_monitor_window():
    """Window for monitoring posture."""
    global timer_label, running
    for widget in root.winfo_children():
        widget.grid_forget()

    running = True

    timer_label = tk.Label(root, text="25:00", font=("Arial", 24))
    timer_label.grid(row=0, column=0, pady=20)

    global posture_message_label
    posture_message_label = tk.Label(root, text="Monitoring posture...", font=("Arial", 16), fg="white", width=50, height=4)
    posture_message_label.grid(row=1, column=0, pady=20)

    btn_stop_session = ttk.Button(root, text="Stop Session", style="Accent.TButton", command=stop_session)
    btn_stop_session.grid(row=2, column=0, pady=10)

    threading.Thread(target=monitor_posture, daemon=True).start()
    countdown(25 * 60)

# --- Posture Monitoring Logic ---
def monitor_posture():
    """Monitor posture and update GUI."""
    global running
    while running:
        value = backend.read_flex_value(ser)
        if value is not None:
            if value > baseline + backend.offset:
                posture_message_label.config(text="Uh oh, bad posture detected!", fg="red", bg="white")
            else:
                posture_message_label.config(text="Great job! Your posture is good.", fg="green", bg="white")
        time.sleep(0.5)

# --- Countdown Timer ---
def countdown(time_left):
    """Display countdown timer."""
    if time_left > 0 and running:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"{mins:02}:{secs:02}")
        root.after(1000, countdown, time_left - 1)
    elif time_left == 0:
        messagebox.showinfo("Pomodoro Complete", "Time is up! Take a break and stretch!")
        stop_session()

# --- Stop Session ---
def stop_session():
    """Stop the session and reset to the main window."""
    global running
    running = False
    # Reset background & main label
    theme_bg = style.lookup(".", "background")
    tk.Label(root, text="Connection established. Please calibrate to start!", font=("Arial", 16), fg="green", width=50, height=4)
    root.configure(bg=theme_bg)

    main_window()

# --- Information Window ---
def information_window():
    """Information page."""
    for widget in root.winfo_children():
        widget.grid_forget()

    label_info = tk.Label(root, text="Information Page", font=("Arial", 24), fg="white")
    label_info.grid(row=2, column=0, pady=20)

    btn_back = ttk.Button(root, text="Back", style="Accent.TButton", command=main_window)
    btn_back.grid(row=3, column=0, pady=10)

# --- Initialize Connection ---
def initialize_connection():
    global ser
    if not ser:
        ser = backend.connect_to_arduino()
        if ser:
            posture_message_label.config(text="Connection established! Please calibrate to start.", fg="green", bg="white")
        else:
            posture_message_label.config(text="Connection failed. Check the device!", fg="red", bg="white")

# --- Exit App ---
def exit_app():
    """Exit the application."""
    global running
    running = False
    if ser:
        backend.close_connection(ser)
    root.quit()

# --- Main ---
def on_close():
    """Handle app closure."""
    global running
    running = False
    if ser:
        backend.close_connection(ser)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
main_window()
initialize_connection()
root.mainloop()
