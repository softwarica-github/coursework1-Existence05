import socket
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import logging
import unittest

logging.basicConfig(filename='port_scanner.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_ports(ip, start_port, end_port):
    open_ports = []
    closed_ports = []

    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Set a timeout for the connection attempt
        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            else:
                closed_ports.append(port)
        except socket.error:
            # Handle socket errors (e.g., invalid IP address)
            messagebox.showerror("Error", "Failed to connect to the target.")
            return [], []
        finally:
            s.close()

    return open_ports, closed_ports

class PortScannerTests(unittest.TestCase):
    def test_scan_ports_with_open_port(self):
        ip = '127.0.0.1'
        start_port = 80
        end_port = 81
        open_ports, closed_ports = scan_ports(ip, start_port, end_port)
        self.assertIn(80, open_ports)
        self.assertNotIn(81, open_ports)  
        
    def test_scan_ports_with_closed_port(self):
        ip = '127.0.0.1'
        start_port = 82
        end_port = 83
        open_ports, closed_ports = scan_ports(ip, start_port, end_port)
        self.assertNotIn(82, open_ports)
        self.assertIn(83, closed_ports)

def on_scan_button_click():
    ip = ip_entry.get()
    start_port_str = start_port_entry.get()
    end_port_str = end_port_entry.get()

    try:
        start_port = int(start_port_str)
        end_port = int(end_port_str)
        if start_port < 0 or start_port > 65535 or end_port < 0 or end_port > 65535:
            raise ValueError("Port number out of range")
        if end_port < start_port:
            raise ValueError("End port cannot be less than the start port")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}")
        return

    try:
        open_ports, closed_ports = scan_ports(ip, start_port, end_port)
        display_scan_results(open_ports, closed_ports)
    except ValueError:
        messagebox.showerror("Error", "Invalid input. Please enter a valid IP address.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during scanning: {e}")


def display_scan_results(open_ports, closed_ports):
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)  # Clear previous results

    # Display the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result_text.insert(tk.END, f"Scan completed at {current_time}\n\n")

    for port in open_ports:
        result_text.insert(tk.END, f"Port {port} is open.\n", "open")
        logging.info(f"Port {port} is open.")

    for port in closed_ports:
        result_text.insert(tk.END, f"Port {port} is closed.\n", "closed")

    result_text.config(state=tk.DISABLED)

def on_clear_button_click():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)

def on_close_button_click():
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Port Scanner")
root.configure(bg="light gray")  # Set background color

# IP Address
ip_label = tk.Label(root, text="Enter IP address:")
ip_label.pack(pady=5)
ip_entry = tk.Entry(root)
ip_entry.pack(pady=5)

# Port Range
ports_label = tk.Label(root, text="Enter port range (start, end):")
ports_label.pack(pady=5)
start_port_entry = tk.Entry(root)
start_port_entry.pack(pady=5)
end_port_entry = tk.Entry(root)
end_port_entry.pack(pady=5)

# Result Display
result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.tag_configure("open", foreground="green")
result_text.tag_configure("closed", foreground="red")
result_text.pack(pady=10)

# Scan Button
scan_button = tk.Button(root, text="Scan Ports", command=on_scan_button_click)
scan_button.pack(pady=5)

# Clear Button
clear_button = tk.Button(root, text="Clear Results", command=on_clear_button_click)
clear_button.pack(pady=5)

# Close Button
close_button = tk.Button(root, text="Close", command=on_close_button_click)
close_button.pack(pady=5)

# Run the GUI
if __name__ == "__main__":
    unittest.main(argv=[''], exit=False)

root.mainloop()
