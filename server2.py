import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Function to handle receiving messages from the client
def handle_client(client_socket, text_area):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            text_area.insert(tk.END, f"Client: {data.decode('utf-8')}\n", 'client')
        except OSError:
            break

    client_socket.close()

# Function to start the server
def start_server(text_area):
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind(("10:68:38:c2:43:e5", 4))
    server.listen(2)
    
    text_area.insert(tk.END, "Waiting for connection...\n", 'info')
    client_socket, addr = server.accept()
    text_area.insert(tk.END, f"Connected to {addr}\n", 'info')
    
    # Start a new thread to handle incoming messages
    threading.Thread(target=handle_client, args=(client_socket, text_area)).start()

    def send_message():
        message = entry.get()
        entry.delete(0, tk.END)
        client_socket.send(message.encode("utf-8"))
        text_area.insert(tk.END, f"You: {message}\n", 'user')

    # Configure send button action
    send_button.config(command=send_message)

# Create the server interface
root = tk.Tk()
root.title("Bluetooth Server Chatbox")

# Set the main window background color
root.configure(bg="#2e3f4f")

# Create a text area with scroll functionality
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#1f2a35", fg="white", font=("Arial", 12), height=15)
text_area.pack(padx=10, pady=10, fill=tk.BOTH)

# Configure tags for colored text
text_area.tag_config('client', foreground='#f28b82')
text_area.tag_config('user', foreground='#a7ffeb')
text_area.tag_config('info', foreground='#fbbc05', font=("Arial", 12, "italic"))

# Entry box for user input
entry = tk.Entry(root, bg="#394a5b", fg="white", font=("Arial", 12))
entry.pack(padx=10, pady=5, fill=tk.X)

# Send button
send_button = tk.Button(root, text="Send", bg="#5c6bc0", fg="white", font=("Arial", 12))
send_button.pack(padx=10, pady=5)

# Start the server when the GUI is loaded
threading.Thread(target=start_server, args=(text_area,)).start()

root.mainloop()
