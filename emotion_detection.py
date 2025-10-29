import cv2
import numpy as np
from fer import FER
from collections import deque
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
from PIL import Image

class EmotionDetector:
    """
    A class to handle emotion detection, logging, and visualization.
    """
    def __init__(self, mtcnn=True):
        """
        Initializes the EmotionDetector.

        :param mtcnn: Whether to use the MTCNN face detector.
        """
        self.detector = FER(mtcnn=mtcnn)
        self.emotion_pulse = deque(maxlen=10)
        self.pulse_log = pd.DataFrame(columns=["Timestamp", "Emotion"])
        print("✅ FER Emotion Detector ready!")

    def analyze_emotion(self, image_path):
        """
        Analyzes the emotion from an image file.

        :param image_path: The path to the image file.
        :return: A tuple of (dominant_emotion, score).
        """
        img = cv2.imread(image_path)
        if img is None:
            try:
                # Fallback for images that cv2 can't open directly
                img = cv2.cvtColor(np.array(Image.open(image_path)), cv2.COLOR_RGB2BGR)
            except Exception as e:
                print(f"Error reading image: {e}")
                return None, None

        dominant_emotion, score = self.detector.top_emotion(img)

        if dominant_emotion is None:
            # If no face is detected, we can default to "neutral"
            dominant_emotion = "neutral"
            score = 0.0

        # Log the emotion
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.emotion_pulse.append(dominant_emotion)
        self.pulse_log.loc[len(self.pulse_log)] = [timestamp, dominant_emotion]

        return dominant_emotion, score

    def plot_timeline(self):
        """
        Plots the timeline of detected emotions.
        """
        if self.pulse_log.empty:
            print("No emotion data logged yet.")
            return

        plt.figure(figsize=(12, 6))

        # Convert timestamp to datetime objects for plotting
        timestamps = pd.to_datetime(self.pulse_log["Timestamp"])

        sns.lineplot(x=timestamps, y=self.pulse_log.index, marker='o', linestyle='-')

        # Annotate points with emotion labels
        for i, (ts, emotion) in enumerate(zip(timestamps, self.pulse_log["Emotion"])):
            plt.text(ts, i, f" {emotion}", verticalalignment='center')

        plt.title("Emotion Timeline", fontsize=16)
        plt.xlabel("Time")
        plt.ylabel("Emotion Events")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_log(self, filename="emotion_log.csv"):
        """
        Saves the emotion log to a CSV file.

        :param filename: The name of the file to save the log to.
        """
        try:
            self.pulse_log.to_csv(filename, index=False)
            print(f"Emotion log saved to {filename}")
        except Exception as e:
            print(f"Error saving log: {e}")

    def get_current_pulse(self):
        """
        Gets the most frequent emotion in the current rolling window.
        """
        if not self.emotion_pulse:
            return "N/A"
        counts = {e: self.emotion_pulse.count(e) for e in set(self.emotion_pulse)}
        return max(counts, key=counts.get)
