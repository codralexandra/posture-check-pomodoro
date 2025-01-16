import serial
import time

arduino_port = 'COM6'  # Replace with your port (please)
baud_rate = 9600
offset = 10 # Adjust the offset value after wearing (please again)

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

def read_flex_values(ser):
    """
    Read values for four sensors from the Arduino serial connection.
    The Arduino should send data in the format: "value1,value2,value3,value4\n"
    """
    try:
        if ser.in_waiting > 0:  # Check if data is available
            data = ser.readline().decode('utf-8').strip()  # Read and decode the line
            sensor_values = data.split(",")  # Split the line into sensor values
            
            # Ensure exactly 4 values are received
            if len(sensor_values) == 4:
                try:
                    # Convert sensor values to integers
                    flex1, flex2, flex3, flex4 = map(int, sensor_values)
                    print(f"Sensor 1: {flex1}, Sensor 2: {flex2}, Sensor 3: {flex3}, Sensor 4: {flex4}")
                    return flex1, flex2, flex3, flex4  # Return the sensor values as a tuple
                except ValueError:
                    print("Error: Non-integer value received in sensor data.")
                    return None
            else:
                print("Error: Incomplete data received. Expected 4 values.")
                return None
        else:
            return None  # No data available
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
    if ser:
        try:
            print("Reading flex sensor values. Press Ctrl+C to stop.")
            while True:
                value = read_flex_values(ser)
                if value is not None:
                    print(f"Flex value: {value}")
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            close_connection(ser)
