from PCANBasic import *
import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class CANReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CAN Reader Application")
        
        # Initialize PCAN-Basic
        self.pcan_basic = PCANBasic()
        self.channel = PCAN_USBBUS1
        self.baudrate = PCAN_BAUD_500K
        self.pcan_basic.Initialize(self.channel, self.baudrate)
        
        # GUI Elements
        self.msg_list = tk.Listbox(self.root, height=25, width=100)
        self.msg_list.pack(padx=10, pady=10)

        # Thread for reading CAN messages
        self.read_thread = threading.Thread(target=self.read_messages)
        self.read_thread.daemon = True
        self.read_thread.start()

        # Setup graph
        self.setup_graph()

    def setup_graph(self):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.x_data = []
        self.y_data = []
        self.start_time = time.time()
        
    def update_graph(self, battery_percentage, temperature):
        current_time = time.time() - self.start_time
        self.x_data.append(current_time)
        self.y_data.append(battery_percentage)
        self.y_data_temp.append(temperature)  # Append new temperature data

        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data_battery, color='blue', label='Battery (V)')
        self.ax.plot(self.x_data, self.y_data_temp, color='red', label='Temperature (°C)')  # Plot temperature data
        self.ax.set_title('Battery Voltage Over Time')
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Value')
        self.ax.legend()

        # Set a fixed width for the x-axis (e.g., last 60 seconds)
        time_window = 60  # seconds
        if current_time > time_window:
            self.ax.set_xlim(current_time - time_window, current_time)
        else:
            self.ax.set_xlim(0, time_window)

        self.canvas.draw()


    def read_messages(self):
        id_filter = 0x001
        while True:
            result = self.pcan_basic.Read(self.channel)
            if result[0] == PCAN_ERROR_OK:
                message = result[1]
                if message.ID == id_filter:
                    self.display_message(message)
                    battery_percentage = message.DATA[0]
                    temperature = message.DATA[1]
                    self.update_graph(battery_percentage, temperature)

    def display_message(self, message):
        # Format the message for display
        msg_str = f"ID: {message.ID}, Data: {message.DATA[:message.LEN]}"
        self.msg_list.insert(tk.END, msg_str)

def main():
    root = tk.Tk()
    app = CANReaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
