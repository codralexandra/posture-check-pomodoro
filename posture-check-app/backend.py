import serial
import time

arduino_port = 'COM6'  # Replace with your port
baud_rate = 9600
threshold = 600 

def connect_to_arduino():
    """Connect to the Arduino and return the serial connection."""
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
        time.sleep(2)
        print("Connected to Arduino")
        return ser
    except serial.SerialException as e:
        print(f"Error: {e}")
        return None

def read_flex_value(ser):
    """Read a single value from the Arduino serial connection."""
    try:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            if data.isdigit():
                return int(data)
        return None
    except Exception as e:
        print(f"Error reading data: {e}")
        return None

def close_connection(ser):
    """Close the Arduino serial connection."""
    if ser and ser.is_open:
        ser.close()
        print("Connection closed.")

if __name__ == '__main__':
    ser = connect_to_arduino()
    print(read_flex_value(ser))