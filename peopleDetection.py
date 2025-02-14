import cv2
import asyncio
from pytz import timezone
from datetime import datetime
from ultralytics import YOLO
import customtkinter as ctk
from tkinter.font import Font
from typing import Optional, Union, Any

class MyVideoCapture(cv2.VideoCapture):
    """ Context manager wrapper for cv2.VideoCapture"""
    def __enter__(self) -> 'MyVideoCapture':
        return self
        
    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        self.release()

class UserInterfaceWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        
        # Set the default appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.height: int = 500
        self.width: int = 500
        
        self._center()
        self.attributes("-topmost", True)
        self.resizable(False, True)

        # Configure main window grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # getting the camera Index
        self.camera_index: int = self.get_camera_index()

        # Initialize YOLO model once
        self.model = YOLO("yolov8n.pt")

        self.setup_ui()

    def _center(self) -> None:
        """ 
        Centers the application window on the screen based on the main screen dimensions
        and window size.
        """
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()

        x: int = (screen_width - self.width) // 2
        y: int = (screen_height - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

    
    def setup_ui(self) -> None:
        """ Sets up the user interface components."""

        # Title label using CTkLabel
        self.title_label: ctk.CTkLabel = ctk.CTkLabel(
            self,
            text="People Detection System",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold")
        )
        self.title_label.grid(row=0, column=0, pady=40, padx=50)

        # Run button using CTkButton
        self.call_button: ctk.CTkButton = ctk.CTkButton(
            self,
            text="Run",
            command=lambda: asyncio.run(self.capture_and_count_people()),  # Runs async function
            font=ctk.CTkFont(size=16),
            height=40
        )
        self.call_button.grid(row=1, column=0, pady=40, padx=50)

        # Create a frame to contain the text box and scrollbar
        self.text_frame: ctk.CTkFrame = ctk.CTkFrame(self)
        self.text_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        self.text_frame.grid_rowconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)

        # Create textbox with scrollbar
        self.text_box: ctk.CTkTextbox = ctk.CTkTextbox(
            self.text_frame,
            font=ctk.CTkFont(family="Arial", size=20),
            wrap="word",
            height=200,
        )
        self.text_box.grid(row=0, column=0, sticky="nsew")

        # Add traditional scrollbar for better visibility
        self.scrollbar: ctk.Scrollbar = ctk.CTkScrollbar(self.text_frame, command=self.text_box.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Link scrollbar and textbox
        self.text_box.configure(yscrollcommand=self.scrollbar.set)

        # Configure the text box
        self.text_box.configure(state="disabled")


    def get_camera_index(self) -> int:
        """ 
        Searches for available cameras and returns the preferred camera index.
        Prioritizes external cameras over the built-in webcam.
        
        Returns:
            int: Index of the preferred camera (0 for built-in, higher numbers for external)
        """

        for i in range(1, 5):  # Checking for external cameras
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                cap.release()
                return i

        return 0


    async def capture_and_count_people(self) -> None:
        """Captures a frame asynchronously and processes YOLO detection without blocking the UI."""

        # Disable the button while processing
        self.call_button.configure(state="disabled")

        # Run the blocking code in a separate thread
        message = await asyncio.to_thread(self.process_camera)

        self.write(text=message)  # Display user-facing messages in the UI

        self.call_button.configure(state="normal")


    def process_camera(self) -> str:
        """Processes the camera capture and person detection, returning (message)."""
        
        with MyVideoCapture(self.camera_index) as cap:
            if not cap.isOpened():
                print("hii")
                return "Error: No camera detected."

            _, frame = cap.read()
            print("got here")

            # Perform detection, but ONLY for 'person' (class 0)
            results = self.model(frame, classes=[0])
            num_people = len(results[0].boxes)
            print("got here2")


        return f"Number of people detected: {num_people}"

    def write(self, text: str) -> None:
        """
        Writes timestamped messages to the text box.
        
        Args:
            text (str): message to be written.            
        Note:
            At least one of text or people_count must be provided.
        """
        time_zone = timezone("Israel")
        date_time = datetime.now(time_zone)
        formatted_time: str = date_time.strftime("%H:%M:%S")
        message: str = f"({formatted_time}) {text}\n"
        print("got here3")

        self.text_box.configure(state="normal")
        self.text_box.insert("end", message)
        self.text_box.configure(state="disabled")
        self.text_box.see("end")  # Auto-scroll to the bottom
        print("got here4")


if __name__ == "__main__":
    app = UserInterfaceWindow()
    app.mainloop()