import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Function to handle receiving messages from the server
def receive_messages(client_socket, text_area):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            text_area.insert(tk.END, f"Server: {data.decode('utf-8')}\n", 'server')
        except OSError:
            break

    client_socket.close()

# Function to start the client
def start_client(text_area):
    client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client_socket.connect(("10:68:38:c2:43:e5", 4))
    text_area.insert(tk.END, "Connected to the server.\n", 'info')

    # Start a new thread to receive messages from the server
    threading.Thread(target=receive_messages, args=(client_socket, text_area)).start()

    def send_message():
        message = entry.get()
        entry.delete(0, tk.END)
        client_socket.send(message.encode("utf-8"))
        text_area.insert(tk.END, f"You: {message}\n", 'user')

    # Configure send button action
    send_button.config(command=send_message)

# Create the client interface
root = tk.Tk()
root.title("Bluetooth Client Chatbox")

# Set the main window background color
root.configure(bg="#2e3f4f")

# Create a text area with scroll functionality
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1f2a35", fg="white", font=("Arial", 12), height=15)
text_area.pack(padx=10, pady=10, fill=tk.BOTH)

# Configure tags for colored text
text_area.tag_config('server', foreground='#f28b82')
text_area.tag_config('user', foreground='#a7ffeb')
text_area.tag_config('info', foreground='#fbbc05', font=("Arial", 12, "italic"))

# Entry box for user input
entry = tk.Entry(root, bg="#394a5b", fg="white", font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(root, text="Send", bg="#5c6bc0", fg="white", font=("Arial", 12))
send_button.pack(padx=10, pady=5)

# Start the client when the GUI is loaded
threading.Thread(target=start_client, args=(text_area,)).start()

root.mainloop()