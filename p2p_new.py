import socket
import pyaudio
import threading
import tkinter as tk
from tkinter import messagebox


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
PORT = 5000
PEER_IP = "10.0.0.3"  


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))  

audio = pyaudio.PyAudio()
output_stream = None
input_stream = None
running = False 

def start_voip():
    global output_stream, input_stream, running
    running = True
    
    output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    threading.Thread(target=receive_audio, daemon=True).start()
    threading.Thread(target=send_audio, daemon=True).start()
    status_label.config(text="Status: Call in progress")

def stop_voip():
    global running
    running = False
    status_label.config(text="Status: Call ended")

def receive_audio():
    while running:
        try:
            data, addr = sock.recvfrom(CHUNK * 2)
            if output_stream:
                output_stream.write(data)
        except Exception as e:
            print("Receive Error:", e)

def send_audio():
    while running:
        try:
            data = input_stream.read(CHUNK, exception_on_overflow=False)
            sock.sendto(data, (PEER_IP, PORT))
        except Exception as e:
            print("Send Error:", e)


root = tk.Tk()
root.title("VoIP App")
root.geometry("300x200")

status_label = tk.Label(root, text="Status: Idle", font=("Arial", 12))
status_label.pack(pady=20)

start_button = tk.Button(root, text="Start Call", command=start_voip, bg="green", fg="white", font=("Arial", 12))
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Call", command=stop_voip, bg="red", fg="white", font=("Arial", 12))
stop_button.pack(pady=5)

root.mainloop()
