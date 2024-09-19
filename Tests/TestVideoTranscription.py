import unittest
from unittest.mock import MagicMock, patch
import cv2
from ultralytics import YOLO
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from VideoTranscription import detect_object_in_video

class TestObjectDetection(unittest.TestCase):

    @patch('cv2.VideoCapture')
    @patch('ultralytics.YOLO')
    def test_detect_object_in_video(self, mock_yolo, mock_videocapture):
        # Mock the YOLO model
        mock_model = mock_yolo.return_value

        # Simulate the class names (class_ids)
        mock_model.names = ['apple', 'car', 'dog']  # Example class names

        # Simulate object detection results
        mock_result = MagicMock()
        mock_box = MagicMock()
        mock_box.cls = [1]  # Class ID for 'car'
        mock_result.boxes = [mock_box]

        # Simulate the YOLO model returning this result
        mock_model.predict.return_value = [mock_result]

        # Mock VideoCapture to simulate video reading
        mock_cap = mock_videocapture.return_value
        mock_cap.isOpened.side_effect = [True] * 100 + [False]  # Simulate video of 3 frames
        mock_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        mock_cap.read.side_effect = [(True, mock_frame)] * 100 + [(False, None)]
        mock_cap.get.return_value = 30.0  # Assume 30 fps for video

        # Define the input arguments
        video_path = 'fruit-and-vegetable-detection.mp4'
        user_object = 'apple'  # Object we're looking for

        # Call the detect_object_in_video function
        timestamps = detect_object_in_video(video_path, user_object, check_interval=1)

        # Check the results
        self.assertGreater(len(timestamps), 0, "No object was detected when it should have been.")
        print("Timestamps:", timestamps)

        # Verify that VideoCapture was called with the correct video path
        mock_videocapture.assert_called_once_with(video_path)

        # Ensure YOLO model was called to detect objects
        mock_model.predict.assert_called()