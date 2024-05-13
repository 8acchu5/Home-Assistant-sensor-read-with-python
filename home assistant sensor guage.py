import requests
import time
import json
import tkinter as tk

# Read API token from secrets file
with open("secrets.txt", "r") as f:
    api_token = f.read().strip("API_TOKEN=")
    
# Home Assistant server IP address
hass_server = "192.168.5.10:8123"

# API endpoints for sensor data
api_endpoint_mines_temp = f"http://{hass_server}/api/states/sensor.thermometer_mines_temperature"
api_endpoint_outside_temp = f"http://{hass_server}/api/states/sensor.outside_temp_sensor_temperature"

# Home Assistant API token
API_TOKEN="YOUR_API_TOKEN"
#api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI1NTcyYjFkNzBjZWM0M2MwOTI4ZWZjZDY1ZWU4YTdiYyIsImlhdCI6MTcxNTU1MTEyNiwiZXhwIjoyMDMwOTExMTI2fQ.WDi9zNqojdYWyKLwkwlAzJOAS-YQyfBlOE8sLjvcjhc"

# Headers for API request
headers = {"Authorization": f"Bearer {api_token}"}

# Create a Tkinter window
window = tk.Tk()
window.title("Temperature Sensors")

# Create labels to display sensor values
label_mines_temp = tk.Label(window, font=("Arial", 24))
label_outside_temp = tk.Label(window, font=("Arial", 24))

# Position the labels
label_mines_temp.pack()
label_outside_temp.pack()

# Function to update sensor values
def update_sensor_values():
    # Send GET requests to API endpoints
    response_mines_temp = requests.get(api_endpoint_mines_temp, headers=headers)
    response_outside_temp = requests.get(api_endpoint_outside_temp, headers=headers)

    # Check for successful responses
    if response_mines_temp.status_code == 200 and response_outside_temp.status_code == 200:
        # Parse JSON responses
        data_mines_temp = response_mines_temp.json()
        data_outside_temp = response_outside_temp.json()

        # Extract sensor values
        mines_temp = data_mines_temp["state"]
        outside_temp = data_outside_temp["state"]

        # Update labels with sensor values
        label_mines_temp["text"] = f"Thermometer Mines Temperature: {mines_temp}°C"
        label_outside_temp["text"] = f"Outside Temperature: {outside_temp}°C"
    else:
        label_mines_temp["text"] = f"Error getting sensor data: {response_mines_temp.status_code}"
        label_outside_temp["text"] = f"Error getting sensor data: {response_outside_temp.status_code}"

    # Schedule the next update in 30 seconds
    window.after(30000, update_sensor_values)

# Start sensor value update process
update_sensor_values()

print(api_token)

# Run Tkinter event loop
window.mainloop()