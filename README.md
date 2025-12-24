# Minimalist YOLO: Real-time Assistive Vision

**Group 10**
Kevin (1143501), York (1143513), George (1143515), Jeremy (1143524)

## Project Description
This project validates "Minimalism" in assistive technology. It uses YOLOv8n to provide low-latency, zero-shot object detection with voice feedback for visually impaired users. The system is designed to run on low-resource hardware using a pure software implementation.

## Features
* **Real-time Detection:** Uses the lightweight YOLOv8n model.
* **Voice Feedback:** Integrates `win32com.client` (SAPI) for offline text-to-speech alerts.
* **Fault Tolerance:** Includes error handling for webcam and speech engine conflicts.

## Installation & Setup

1.  **Create Environment**
    Open your terminal (Anaconda Prompt) and run:
    ```bash
    conda create -n yolo_blind python=3.10
    conda activate yolo_blind
    ```

2.  **Install Dependencies**
    Install the required libraries (YOLOv8, OpenCV, and Windows Audio support):
    ```bash
    pip install ultralytics opencv-python pypiwin32
    ```

3.  **Run the System**
    Navigate to the project folder and execute the script:
    ```bash
    python yolo_identifier.py
    ```

## Usage
* Ensure your webcam is connected.
* The system will audibly announce detected objects (e.g., "Alert! I see a cup").
* Press `q` on your keyboard to exit the application.
