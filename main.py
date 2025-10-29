import cv2
from emotion_detection import EmotionDetector
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

def main():
    """
    Main function to run the emotion detection application.
    """
    emotion_detector = EmotionDetector()

    while True:
        print("\nMenu:")
        print("1. Capture Photo and Analyze Emotion")
        print("2. View Emotion Timeline")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # In a local environment, we'll use opencv to capture an image from the webcam
            # The take_photo function from the notebook is browser-specific.
            print("Opening webcam... Press 'c' to capture or 'q' to quit.")
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("Error: Could not open webcam.")
                continue

            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture image.")
                    break
                cv2.imshow('Webcam - Press "c" to capture, "q" to quit', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('c'):
                    # Save the captured frame to a file
                    photo_filename = "photo.jpg"
                    cv2.imwrite(photo_filename, frame)
                    cap.release()
                    cv2.destroyAllWindows()

                    # Analyze the captured photo
                    dominant_emotion, score = emotion_detector.analyze_emotion(photo_filename)

                    if dominant_emotion:
                        print(f"Dominant Emotion: {dominant_emotion.capitalize()} (Score: {score:.2f})")

                        # Display the image with the emotion
                        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        plt.figure(figsize=(6, 4))
                        plt.imshow(img)
                        plt.axis('off')
                        plt.title(f"{dominant_emotion.capitalize()} — score: {score:.2f}", fontsize=14)
                        plt.show()

                    else:
                        print("No face detected or emotion could not be determined.")

                    break
                elif key == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    break

        elif choice == '2':
            emotion_detector.plot_timeline()

        elif choice == '3':
            print("Exiting...")
            emotion_detector.save_log()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
