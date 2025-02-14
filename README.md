# People Detection System

This application uses YOLOv8 to detect people in real-time through a webcam feed. The system includes a graphical user interface (GUI) built with `customtkinter`, and the camera feed is processed asynchronously to prevent UI freezes. The app will display the number of people detected in the webcam feed and show timestamped messages in the text area.

## Features

- Real-time people detection using YOLOv8.
- A user-friendly interface with a "Run" button to trigger the detection.
- Display of the number of people detected with timestamps.
- Automatic camera detection, prioritizing external cameras.
- Modern dark-themed interface powered by `customtkinter`.

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
