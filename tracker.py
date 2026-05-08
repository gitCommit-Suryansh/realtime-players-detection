import cv2
import numpy as np
from collections import defaultdict, deque
from ultralytics import YOLO
from config import MODEL_NAME, TRACKER_TYPE, TARGET_CLASSES, CONFIDENCE_THRESHOLD

class VideoTracker:
    def __init__(self):
        print(f"Loading YOLO model: {MODEL_NAME}...")
        self.model = YOLO(MODEL_NAME)
        # Store trajectory history for each track ID (max 30 frames)
        self.track_history = defaultdict(lambda: deque(maxlen=30))
        print("Model loaded successfully.")

    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {input_path}")
            return False

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Setup video writer
        # Reverted back to mp4v because avc1 (H.264) requires external OpenH264 DLL on Windows.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        print(f"Processing video: {input_path}")
        print(f"Resolution: {width}x{height}, FPS: {fps}, Total Frames: {total_frames}")

        frame_count = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processing frame {frame_count}/{total_frames}...")

            # Run tracking
            # persist=True enables tracking across frames
            # classes filters for target classes
            results = self.model.track(
                frame, 
                persist=True, 
                tracker=TRACKER_TYPE, 
                classes=TARGET_CLASSES,
                conf=CONFIDENCE_THRESHOLD,
                verbose=False
            )

            # Visualize the results on the frame (Bounding boxes + IDs)
            annotated_frame = results[0].plot()

            # --- Optional Enhancements ---
            boxes = results[0].boxes
            
            # 1. Object Count Over Time
            obj_count = len(boxes) if boxes is not None else 0
            cv2.putText(annotated_frame, f"Active Objects: {obj_count}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            # 2. Trajectory Visualization
            if boxes is not None and boxes.id is not None:
                track_ids = boxes.id.int().cpu().tolist()
                # Get the center coordinates for each box (xywh format: x_center, y_center, width, height)
                centers = boxes.xywh.cpu().tolist()
                
                for track_id, center in zip(track_ids, centers):
                    x, y = int(center[0]), int(center[1])
                    track = self.track_history[track_id]
                    track.append((x, y))
                    
                    # Draw the trajectory line
                    if len(track) > 1:
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 255), thickness=3) # Yellow line
            # -----------------------------

            # Write the annotated frame to the output video
            out.write(annotated_frame)

        cap.release()
        out.release()
        print(f"Finished processing. Output saved to {output_path}")
        return True

    def process_video_stream(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {input_path}")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # We must use 'mp4v' or 'H264' (if available). Streamlit sometimes struggles with mp4v playback in browser.
        # But for saving and downloading, mp4v is standard in OpenCV.
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break
                
            frame_count += 1
            
            results = self.model.track(
                frame, persist=True, tracker=TRACKER_TYPE, 
                classes=TARGET_CLASSES, conf=CONFIDENCE_THRESHOLD, verbose=False
            )

            annotated_frame = results[0].plot()

            boxes = results[0].boxes
            obj_count = len(boxes) if boxes is not None else 0
            cv2.putText(annotated_frame, f"Active Objects: {obj_count}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            if boxes is not None and boxes.id is not None:
                track_ids = boxes.id.int().cpu().tolist()
                centers = boxes.xywh.cpu().tolist()
                for track_id, center in zip(track_ids, centers):
                    x, y = int(center[0]), int(center[1])
                    track = self.track_history[track_id]
                    track.append((x, y))
                    if len(track) > 1:
                        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 255, 255), thickness=3)

            # Write full-resolution frame to the output video
            out.write(annotated_frame)
            
            # --- Performance Optimization for Streamlit UI ---
            # Yield only every 2nd frame to reduce WebSocket lag
            if frame_count % 2 == 0:
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                # Resize the frame down to 800px width for fast UI rendering
                h, w, _ = rgb_frame.shape
                if w > 800:
                    scale = 800 / w
                    dim = (800, int(h * scale))
                    rgb_frame = cv2.resize(rgb_frame, dim, interpolation=cv2.INTER_AREA)
                    
                yield rgb_frame

        cap.release()
        out.release()
