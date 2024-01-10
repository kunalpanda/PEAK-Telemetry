from PCANBasic import *
import tkinter as tk
from tkinter import ttk
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import cantools  # Import cantools for DBC file handling


class CANReaderApp:
    def __init__(self, root, dbc_path):
        self.root = root
        self.root.title("CAN Reader Application")

        self.filters = {}

        # Load the DBC file
        self.dbc = cantools.database.load_file(dbc_path)

        # create windows for different battery modules
        self.M1_window = self.create_M1_window()
        self.M1_window.withdraw()  # This hides the window

        # Button to display DBC information
        dbc_button = tk.Button(self.root, text="Show DBC Info", command=self.display_dbc_info)
        dbc_button.pack(pady=5)

        # Buttons for each battery pack
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        # Buttons for each battery pack
        M1_button = tk.Button(button_frame, text="M1 Voltages", command=self.display_M1_Voltages)
        M1_button.grid(row=0, column=0, padx=5)

        M2_button = tk.Button(button_frame, text="M2 Voltages", command=self.display_dbc_info)
        M2_button.grid(row=0, column=1, padx=5)

        M3_button = tk.Button(button_frame, text="M3 Voltages", command=self.display_dbc_info)
        M3_button.grid(row=0, column=2, padx=5)

        M4_button = tk.Button(button_frame, text="M4 Voltages", command=self.display_dbc_info)
        M4_button.grid(row=0, column=3, padx=5)

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

    def display_dbc_info(self):
        # Create a new window
        dbc_info_window = tk.Toplevel(self.root)
        dbc_info_window.title("DBC File Information")

        # Text widget to display DBC information
        dbc_text = tk.Text(dbc_info_window, height=50, width=110)
        dbc_text.pack(padx=10, pady=10)

        # Decode DBC file and display information
        for message in self.dbc.messages:
            if "CellVoltages" in message.name:
                msg_info = f"Message: {message.name}, ID: {message.frame_id}, Length: {message.length}\n"
                dbc_text.insert(tk.END, msg_info)
                for signal in message.signals:
                    signal_info = f"  Signal: {signal.name}, Start: {signal.start}, Length: {signal.length}, Scale: {signal.scale}, Offset: {signal.offset}"
                    if signal.unit:
                        signal_info += f", Unit: {signal.unit}"
                    if signal.minimum:
                        signal_info += f", Min: {signal.minimum}, Max: {signal.maximum}"
                    signal_info += "\n"
                    dbc_text.insert(tk.END, signal_info)
                dbc_text.insert(tk.END, "\n")

    def create_M1_window(self):
        M1_window = tk.Toplevel(self.root)
        M1_window.title("M1 Voltages")

        # Frame for M1 window buttons
        M1_button_frame = tk.Frame(M1_window)
        M1_button_frame.pack(pady=5)

        # Show M1 DBC Info Button
        M1_dbc_info_button = tk.Button(M1_button_frame, text="Show M1 DBC Info", command=self.display_M1_dbc_info)
        M1_dbc_info_button.grid(row=0, column=0, padx=5)

        # Hide M1 Window Button
        M1_hide_button = tk.Button(M1_button_frame, text="Hide", command=self.hide_M1_window)
        M1_hide_button.grid(row=0, column=1, padx=5)

        M1_text = tk.Text(M1_window, height=10, width=50)
        M1_text.pack(padx=10, pady=10)

        # Store the text widget in an attribute for later access
        self.M1_text = M1_text

        return M1_window

    def display_M1_Voltages(self):
        # Ensure the window is not destroyed, then show it
        if self.M1_window.winfo_exists():
            self.M1_window.deiconify()
        else:
            self.msg_list.insert(tk.END, "Window has been closed, restart the program")

    def hide_M1_window(self):
        # Hide the M1 window instead of destroying it.
        self.M1_window.withdraw()
    def add_Filters(self):
        filter = 0
        self.filters["M1"] = []
        self.filters["M2"] = []
        self.filters["M3"] = []
        self.filters["M4"] = []
        for message in self.dbc.messages:
            if "M1_CellVoltages" in message.name:
                filter = message.frame_id
                self.filters["M1"].append(filter)
            if "M2_CellVoltages" in message.name:
                filter = message.frame_id
                self.filters["M2"].append(filter)
            if "M3_CellVoltages" in message.name:
                filter = message.frame_id
                self.filters["M3"].append(filter)
            if "M4_CellVoltages" in message.name:
                filter = message.frame_id
                self.filters["M4"].append(filter)

    def display_M1_dbc_info(self):
        # Create a new window
        M1_dbc_window = tk.Toplevel(self.root)
        M1_dbc_window.title("M1 DBC Info")

        # Text widget to display DBC information
        dbc_text = tk.Text(M1_dbc_window, height=25, width=100)
        dbc_text.pack(padx=10, pady=10)

        # Decode DBC file and display information
        for message in self.dbc.messages:
            if "M1_CellVoltages" in message.name:
                msg_info = f"Message: {message.name}, ID: {message.frame_id}, Length: {message.length}\n"
                dbc_text.insert(tk.END, msg_info)
                for signal in message.signals:
                    signal_info = f"  Signal: {signal.name}, Start: {signal.start}, Length: {signal.length}, Scale: {signal.scale}, Offset: {signal.offset}"
                    if signal.unit:
                        signal_info += f", Unit: {signal.unit}"
                    if signal.minimum:
                        signal_info += f", Min: {signal.minimum}, Max: {signal.maximum}"
                    signal_info += "\n"
                    dbc_text.insert(tk.END, signal_info)
                dbc_text.insert(tk.END, "\n")

    def read_messages(self):
        self.add_Filters()
        while True:
            result = self.pcan_basic.Read(self.channel)
            if result[0] == PCAN_ERROR_OK:
                message = result[1]
                if message.ID in self.filters["M1"]:
                    self.display_message(message, self.M1_text)


    def display_message(self, message, box):
        # Format the message for display
        msg_str = f"ID: {message.ID}, Data: {message.DATA[:message.LEN]}"
        box.insert(tk.END, msg_str)


def main():
    root = tk.Tk()
    dbc_path = "F24_AMS_CANDB.dbc"
    app = CANReaderApp(root, dbc_path)
    root.mainloop()


if __name__ == "__main__":
    main()
