import tkinter as tk
from tkinter import messagebox
import time
import threading
import backend 

baseline = None
running = False
ser = None

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
            if value > baseline + backend.threshold:
                posture_label.config(text="Uh oh please fix your posture!", bg="red")
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
    """Stop the session."""
    global running
    running = False
    posture_label.config(text="Session stopped.", bg="white")

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

root = tk.Tk()
root.title("Posture Monitor")

posture_label = tk.Label(root, text="Checking connection...", font=("Arial", 16), bg="white", width=50, height=4)
posture_label.pack(pady=20)

timer_label = tk.Label(root, text="25:00", font=("Arial", 24))
timer_label.pack(pady=10)

btn_calibrate = tk.Button(root, text="Calibrate", font=("Arial", 14), command=calibrate, state="disabled")
btn_calibrate.pack(pady=10)

btn_start = tk.Button(root, text="Start Session", font=("Arial", 14), command=start_session, state="disabled")
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Stop Session", font=("Arial", 14), command=stop_session, state="disabled")
btn_stop.pack(pady=10)

def initialize_connection():
    global ser
    ser = backend.connect_to_arduino()
    if ser:
        posture_label.config(text="Connection established! Please calibrate in order to start.", bg="green")
        btn_calibrate.config(state="normal")
        btn_start.config(state="normal")
    else: 
        failure_label = tk.Label(root, text="Connection failed! Please try connecting the board and try again...", font=("Arial", 24), bg="lightcoral", width=50, height=10)
        failure_label.place(relx=0.5, rely=0.5, anchor="center")
        btn_calibrate.config(state="disabled")
        btn_start.config(state="disabled")

        root.update()
        label_width = failure_label.winfo_width()
        label_height = failure_label.winfo_height()
        root.geometry(f"{label_width}x{label_height}")


def on_close():
    backend.close_connection(ser)
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

initialize_connection()

root.mainloop()
