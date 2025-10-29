# Emotion Detection and Mood Timeline

This project is a Python application that detects emotions from a live webcam feed and logs them to create a mood timeline.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Use the application:**
   - A menu will appear in the console.
   - Choose `1` to open your webcam.
     - Press `c` to capture a photo and analyze your emotion.
     - Press `q` to close the webcam.
   - Choose `2` to view your emotion timeline.
   - Choose `3` to exit the application. An `emotion_log.csv` file will be saved in the project directory.
