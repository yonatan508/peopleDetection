# People Detection System

This application provides a real-time people detection system through a webcam feed. It features a user-friendly graphical interface that allows users to detect and count people in their surroundings with a single click. The detected count is displayed along with timestamps, making it useful for monitoring and analysis.

## Features

- Real-time people detection.
- A user-friendly interface with a "Run" button to trigger the detection.
- Display of the number of people detected with timestamps.
- Automatic camera detection, prioritizing external cameras.
- Modern dark-themed interface.

## Requirements

- Python 3.8+
- `opencv-python` for camera access and image processing.
- `ultralytics` for YOLOv8 model.
- `customtkinter` for the custom GUI components.
- `pytz` for time zone handling.
- `asyncio` for non-blocking asynchronous operations.

You can install the required libraries with:

```bash
pip install opencv-python ultralytics customtkinter pytz
```

## Application Screenshot

![image](https://github.com/user-attachments/assets/7ff5d5d4-1eaf-4d91-a432-d4e6a93fd8af)


- The "Run" button starts the detection process.
- The text box at the bottom displays the detection results, showing a timestamp and the number of people detected in the camera feed.
- The example screenshot shows that one person was detected at 16:11:54.

## Acknowledgements

- This project uses the `YOLOv8 model` for people detection.
- `OpenCV` for computer vision and camera handling.
- `CustomTkinter` for creating a modern and customizable Tkinter interface.
