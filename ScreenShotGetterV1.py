import tkinter as tk
import os
import time
from datetime import datetime, timedelta
import subprocess


def add_seconds_to_time(time_str):
    # Parse the time string into a datetime object
    time_format = '%Y-%m-%d %H%M%S'
    time_obj = datetime.strptime(time_str, time_format)

    # Add 5 seconds to the datetime object
    new_time_obj = time_obj + timedelta(seconds=5)

    # Format the new datetime object back to the desired string format
    new_time_str = new_time_obj.strftime(time_format)

    return new_time_str


def sub_seconds_to_time(time_str):
    # Parse the time string into a datetime object
    time_format = '%Y-%m-%d %H%M%S'
    time_obj = datetime.strptime(time_str, time_format)

    # Add 5 seconds to the datetime object
    new_time_obj = time_obj - timedelta(seconds=5)

    # Format the new datetime object back to the desired string format
    new_time_str = new_time_obj.strftime(time_format)

    return new_time_str


def get_current_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H%M%S')
    return formatted_time


def search_recent_screenshot():
    # Get the current time and the time 5 minutes ahead
    current_time = datetime.now()
    future_time = current_time + timedelta(minutes=5)

    # Get the default screenshots directory
    screenshots_dir = os.path.join(os.path.expanduser('~'), 'Pictures', 'Screenshots')

    # Check if the directory exists
    if os.path.isdir(screenshots_dir):
        found_screenshot = None
        for file in os.listdir(screenshots_dir):
            if file.startswith('Screenshot') and file.endswith('.png'):
                parts = file.split()
                if len(parts) == 3:  # Check if the filename format matches 'Screenshot YYYY-MM-DD HHMMSS.png'
                    try:
                        # Extract the timestamp from the filename
                        timestamp_str = parts[1] + ' ' + parts[2].split('.')[0]
                        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H%M%S')
                        # print("The time stamp is", timestamp)
                        # print("Time strap da shnu:" , timestamp_str)

                        # print("Future what??",future_time)
                        timenow = get_current_time()
                        ffuture = add_seconds_to_time(timenow)
                        # print("Current Time",timenow)
                        # print("Future",ffuture)
                        pasttime = sub_seconds_to_time(timenow)
                        # print("The past time is:" ,pasttime)

                        # Check if the screenshot was taken within the time range
                        if (timestamp_str >= pasttime) and (timestamp_str <= ffuture):
                            # print(f"it says {timenow} <= {ffuture}")
                            found_screenshot = os.path.join(screenshots_dir, file)
                            break
                    except ValueError:
                        pass

        if found_screenshot:
            result_label.config(text="Found recent screenshot:\n" + found_screenshot)
            # print(found_screenshot)
            return found_screenshot
        else:
            result_label.config(text="No recent screenshot found in default screenshots directory.")
            return None
    else:
        result_label.config(text="Default screenshots directory not found.")
        return None


def take_screenshot_and_run_function():
    # Open the Snipping Tool using subprocess
    snipping_tool_process = subprocess.Popen(['snippingtool.exe'])

    # Check if the Snipping Tool process is still running
    while True:
        time.sleep(0.1)

        # searches actively for the screenshot while the snipping tool is running
        found_screenshot = search_recent_screenshot()

        # if screenshot found it closes snipping tool
        if found_screenshot:
            print(found_screenshot)  # for debug
            snipping_tool_process.kill()
            break

    # Testing killing the process

    # Wait for the Snipping Tool process to finish
    snipping_tool_process.wait()


# Create the main application window
app = tk.Tk()
app.title("Snipping Tool App")

# Create a label to display the search result
result_label = tk.Label(app, text="")
result_label.pack(padx=20, pady=10)

# Create a button to trigger taking a screenshot and running a function
snip_button = tk.Button(app, text="Snip", command=take_screenshot_and_run_function)
snip_button.pack(padx=20, pady=10)

# Run the application
app.mainloop()

