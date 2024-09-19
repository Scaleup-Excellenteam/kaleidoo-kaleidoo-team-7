from ultralytics import YOLO
import cv2
import os
#import TextProcessor
from TextProcessorSingleton import TextProcessorSingleton

def detect_object_in_video(video_path, user_object, model_path='yolov8s.pt', check_interval=3):
    # Load the YOLOv8 model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video frame rate to calculate timestamps
    fps = cap.get(cv2.CAP_PROP_FPS)

    frames_to_skip = int(fps * check_interval)
    # Initialize variables
    frame_count = 0
    timestamps = []

    # Get the list of class names
    class_names = model.names  # This is a list of class names indexed by class ID

    while cap.isOpened():
        # Set the current frame position to skip frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        # Run object detection
        results = model(frame)

        # Parse detection results
        for result in results:
            boxes = result.boxes  # Boxes object for bounding boxes, scores, class IDs
            for box in boxes:
                class_id = int(box.cls[0])
                class_name = class_names[class_id]
                if class_name == user_object:
                    # Calculate timestamp
                    timestamp = frame_count / fps
                    timestamps.append(timestamp)
                    break  # If the object is found in the frame, move to the next frame
        # Skip frames for the next check
        frame_count += frames_to_skip

    cap.release()

    # Remove duplicates and sort timestamps
    unique_timestamps = sorted(set(timestamps))
    return unique_timestamps

# Format and display the timestamps
def format_timestamp(seconds):
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    millis = int((seconds - minutes * 60 - secs) * 1000)
    return f"{minutes:02d}:{secs:02d}.{millis:03d}"

def process_video_detection(video_path, user_object, timestamps):
    # Initialize the TextProcessor (which uses the centralized DatabaseManager)
    text_processor = TextProcessorSingleton.get_instance()

    # Extract video name
    video_name = os.path.basename(video_path)

    # Format the detection data
    description = f"Detected '{user_object}' in video '{video_name}' at timestamps: {', '.join(format_timestamp(ts) for ts in timestamps)}."

    # Use the TextProcessor's add_text function to add the description and embedding
    text_processor.add_text(description)



