import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time
import threading
import backend

# --- THEME SETUP ---
root = tk.Tk()
root.title("Posture Monitor")
root.geometry("500x400")
root.option_add("*tearOff", False)

root.columnconfigure(0, weight=1)
root.rowconfigure([0, 1, 2], weight=1)

style = ttk.Style(root)
root.tk.call('source', './theme/forest-dark.tcl')
style.theme_use('forest-dark')

title_label = ttk.Label(root, text="Posture Monitor", font=("Arial", 24), anchor="center", justify="center")
title_label.grid(row=0, column=0, pady=10, sticky="nsew")

separator = ttk.Separator(root)
separator.grid(row=1, column=0, pady=10, sticky="ew")

root.grid_columnconfigure(0, weight=1)

# ---GLOBALS----
baseline = None
running = False
ser = None
posture_message_label = tk.Label(root, text="Checking connection...", font=("Arial", 16), fg="white", width=50, height=4)
timer_label = None
is_break_time = False

# ---MAIN-WINDOW ---
def main_window():
    """Main window with Start, Information, Exit buttons."""
    global posture_message_label
    for widget in root.winfo_children():
        widget.grid_forget()

    title_label.grid(row=0, column=0, pady=10, sticky="ew")
    separator.grid(row=1, column=0, pady=10, sticky="ew")
    posture_message_label.grid(row=2, column=0, pady=20)

    btn_start = ttk.Button(root, text="Start Session", style="Accent.TButton", command=start_calibration)
    btn_start.grid(row=3, column=0, pady=10)

    btn_information = ttk.Button(root, text="Information", command=information_window)
    btn_information.grid(row=4, column=0, pady=10)

    btn_exit = ttk.Button(root, text="Exit", command=exit_app)
    btn_exit.grid(row=5, column=0, pady=10)

# ---CALIBRATION-TIMER---
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
        print(baseline)
        posture_monitor_window()
    else:
        messagebox.showerror("Calibration", "Calibration failed. Please try again!")
        main_window()

# ---POSTURE-MONITOR-WINDOW---
def posture_monitor_window():
    """Window for monitoring posture."""
    global timer_label, running, is_break_time

    is_break_time = False  # Initialize break mode state

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
    countdown(1 * 60)  # Start the first 25-minute work session

# --- POSTURE-MONITOR-LOGIC---
def monitor_posture():
    """Monitor posture and update GUI."""
    global running, is_break_time
    while running:
        #baseline=1015
        if not is_break_time:  # Skip monitoring during breaks
            value = backend.read_flex_value(ser)
            #print(value)
            if value is not None:
                if value > baseline + backend.offset:
                    posture_message_label.config(text="Uh oh, bad posture detected!", fg="red", bg="white")
                else:
                    posture_message_label.config(text="Great job! Your posture is good.", fg="green", bg="white")
        time.sleep(0.01)


# ---POMODORO-TIMER---
def countdown(time_left, is_break=False):
    """Display countdown timer and handle alternating work and break sessions."""
    global is_break_time  # Use this to manage the posture monitoring state

    if time_left > 0 and running:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"{mins:02}:{secs:02}")
        if is_break:
            is_break_time = True  # Enable break mode
            posture_message_label.config(text="Break Time", fg="blue", bg="white")
        else:
            is_break_time = False  # Resume work mode
        root.after(1000, countdown, time_left - 1, is_break)
    elif time_left == 0 and running:
        if is_break:
            is_break_time = False  # End break mode
            posture_message_label.config(text="Monitoring posture...", fg="white", bg="white")  # Reset label for work
            messagebox.showinfo("Break Over", "Break time is over! Back to work!")
            countdown(25 * 60, is_break=False)  # Start a 25-minute work session
        else:
            is_break_time = True  # Start break mode
            posture_message_label.config(text="Break Time", fg="blue", bg="white")  # Update label for break
            messagebox.showinfo("Pomodoro Complete", "Time is up! Take a 5-minute break!")
            countdown(5 * 60, is_break=True)  # Start a 5-minute break


# ---STOP-SESSION---
def stop_session():
    """Stop the session and reset to the main window."""
    global running
    running = False
    theme_bg = style.lookup(".", "background")
    tk.Label(root, text="Connection established. Please calibrate to start!", font=("Arial", 16), fg="green", width=50, height=4)
    root.configure(bg=theme_bg)

    main_window()

# ---INFO-WINDOW---
def information_window():
    """Information page."""
    for widget in root.winfo_children():
        widget.grid_forget()

    label_info = tk.Label(root, text="Information Page", font=("Arial", 24), fg="white")
    label_info.grid(row=0, column=0, pady=20)
    
    text_block = tk.Text(
    root,
    wrap="word",
    font=("Arial", 14),
    height=10,
    width=40,
    bd=0,                  # No border
    highlightthickness=0   # No focus highlight border
    )
    text_block.insert("1.0", "This is a text block.\nYou can write multiple lines here.")
    text_block.grid(row=1, column=0, pady=20)
    text_block.config(state="disabled")

    btn_back = ttk.Button(root, text="Back", style="Accent.TButton", command=main_window)
    btn_back.grid(row=3, column=0, pady=10)

# ---INIT-CONNECTION---
def initialize_connection():
    global ser
    if not ser:
        ser = backend.connect_to_arduino()
        if ser:
            posture_message_label.config(text="Connection established! Please calibrate to start.", fg="green", bg="white")
        else:
            posture_message_label.config(text="Connection failed. Check the device!", fg="red", bg="white")

# ---EXIT---
def exit_app():
    """Exit the application."""
    global running
    running = False
    if ser:
        backend.close_connection(ser)
    root.quit()

# ---MAIN---
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