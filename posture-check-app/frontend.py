import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import backend

#------------SET THEME----------------
root = tk.Tk()
root.title("Posture Monitor")
root.option_add("*tearOff", False)

root.columnconfigure(index=0, weight=1)
root.rowconfigure(index=0, weight=1)
root.rowconfigure(index=1, weight=1)
root.rowconfigure(index=2, weight=1)

style = ttk.Style(root)

root.tk.call('source', 'posture-check-app/theme/forest-dark.tcl')

style.theme_use('forest-dark')

title_label = ttk.Label(root, text="Posture Monitor", font=("Arial", 24))
title_label.grid(row=0, column=0, pady=10, sticky="ew")

separator = ttk.Separator(root)
separator.grid(row=1, column=0, pady=10, sticky="ew")

# Global variables
baseline = None
running = False
ser = None
posture_label = tk.Label(root, text="Checking connection...", font=("Arial", 16), bg="white", width=50, height=4)

# Global buttons for the main window
btn_start = None
btn_information = None
btn_exit = None

# Functions to create each window

def main_window():
    """Main window with Start, Information, Exit buttons."""
    global btn_start, btn_information, btn_exit
    posture_label.grid(row=2, column=0, pady=20)

    # Create buttons after the window is set up
    btn_start = tk.Button(root, text="Start Session", font=("Arial", 14), command=start_window)
    btn_start.grid(row=3, column=0, pady=10)

    btn_information = tk.Button(root, text="Information", font=("Arial", 14), command=information_window)
    btn_information.grid(row=4, column=0, pady=10)

    btn_exit = tk.Button(root, text="Exit", font=("Arial", 14), command=exit_app)
    btn_exit.grid(row=5, column=0, pady=10)

    initialize_connection()  # Call after buttons are created

def start_window():
    """Start window with calibration, timer, and posture monitoring."""
    global btn_start, btn_information, btn_exit
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.grid_forget()

    # Calibrate button
    btn_calibrate = tk.Button(root, text="Calibrate", font=("Arial", 14), command=calibrate)
    btn_calibrate.grid(row=2, column=0, pady=10)

    # Timer label
    global timer_label
    timer_label = tk.Label(root, text="25:00", font=("Arial", 24))
    timer_label.grid(row=3, column=0, pady=10)

    # Start/Stop session buttons
    btn_start_session = tk.Button(root, text="Start Pomodoro", font=("Arial", 14), command=start_session)
    btn_start_session.grid(row=4, column=0, pady=10)

    btn_stop_session = tk.Button(root, text="Stop Session", font=("Arial", 14), command=stop_session)
    btn_stop_session.grid(row=5, column=0, pady=10)

def information_window():
    """Information page."""
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.grid_forget()

    label_info = tk.Label(root, text="Information Page", font=("Arial", 24), bg="lightgray")
    label_info.grid(row=2, column=0, pady=20)

    btn_back = tk.Button(root, text="Back to Main", font=("Arial", 14), command=main_window)
    btn_back.grid(row=3, column=0, pady=10)

def exit_app():
    """Exit the application."""
    root.quit()

def calibrate():
    """Calibrate baseline flex sensor value."""
    def update_countdown(remaining):
        if remaining > 0:
            posture_label.config(text=f"Calibrating... Please maintain posture for {remaining} seconds.", bg="yellow")
            root.after(1000, update_countdown, remaining - 1)
        else:
            perform_calibration()

    def perform_calibration():
        global baseline
        values = []
        start_time = time.time()
        while time.time() - start_time < 3:
            value = backend.read_flex_value(ser)
            if value is not None:
                values.append(value)

        if values:
            baseline = sum(values) // len(values)
            print(f"Calibration complete. Baseline: {baseline}")
            messagebox.showinfo("Calibration", f"Calibration complete! You can start working...{baseline}")
            posture_label.config(text="Calibration complete! Ready to start.", bg="green")
        else:
            messagebox.showerror("Calibration", "Failed to calibrate. Please try again!")
            posture_label.config(text="Calibration failed. Please try again.", bg="red")

    posture_label.config(text="Please maintain a correct posture for 5 seconds to calibrate.", bg="yellow")
    root.after(1000, update_countdown, 5)

def monitor_posture():
    """Monitor posture and update GUI."""
    global running
    while running:
        value = backend.read_flex_value(ser)
        if value is not None:
            if value > baseline + backend.offset:
                posture_label.config(text="Uh oh, please fix your posture!", bg="red")
            else:
                posture_label.config(text="Great job, your posture is great!", bg="green")
        time.sleep(0.1)

def start_session():
    """Start the pomodoro session."""
    global running, baseline
    if not baseline:
        messagebox.showwarning("Warning", "Please calibrate first!")
        return
    
    running = True
    threading.Thread(target=monitor_posture, daemon=True).start()
    countdown(25 * 60)

def stop_session():
    """Stop the session and reset the timer."""
    global running
    running = False
    posture_label.config(text="Session stopped.", bg="white")
    timer_label.config(text="25:00")
    btn_start.config(state="normal")

def countdown(time_left):
    """Display countdown timer."""
    if time_left > 0:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"{mins:02}:{secs:02}")
        root.after(1000, countdown, time_left - 1)
    else:
        messagebox.showinfo("Pomodoro Complete", "Time is up! Take a break and stretch!")
        stop_session()

# --- GUI SETUP ---
posture_label.grid(row=2, column=0, pady=20)

def initialize_connection():
    global ser
    ser = backend.connect_to_arduino()
    if ser:
        posture_label.config(text="Connection established! Please calibrate in order to start.", bg="green")
        btn_start.config(state="normal")
    else:
        failure_label = tk.Label(root, text="Connection failed! Please connect the board and try again...", font=("Arial", 24), bg="lightcoral", width=50, height=10)
        failure_label.place(relx=0.5, rely=0.5, anchor="center")
        btn_start.config(state="disabled")

        root.update()
        label_width = failure_label.winfo_width()
        label_height = failure_label.winfo_height()
        root.geometry(f"{label_width}x{label_height}")

def on_close():
    backend.close_connection(ser)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

main_window()  # Now called before initialize_connection

root.mainloop()
