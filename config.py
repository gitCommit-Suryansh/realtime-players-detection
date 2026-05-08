import os

# Model configuration
MODEL_NAME = "yolov8m.pt"  # Medium model for balance between speed and accuracy
TRACKER_TYPE = "custom_botsort.yaml"  # Custom configuration for fast objects

# Tracking targets (COCO class indices)
# 0: person, 32: sports ball
TARGET_CLASSES = [0, 32]

# Confidence threshold for detections
CONFIDENCE_THRESHOLD = 0.2

# I/O Directories
INPUT_DIR = "data"
OUTPUT_DIR = "output"

# Ensure directories exist
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
