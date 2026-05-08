# Technical Report: Multi-Object Detection and Tracking

**Original Video Source:** [Vecteezy - Football Players Kicking The Ball](https://www.vecteezy.com/video/28545534-football-players-kicking-the-ball-on-pre-game-train)

## 1. Model & Tracker Choices

**Detector:** YOLOv8 Medium (`yolov8m.pt`)
- **Reasoning:** YOLOv8 is a state-of-the-art, single-stage object detector. The medium variant (`yolov8m`) was chosen as it provides the optimal balance between inference speed and detection accuracy for sports footage. It is powerful enough to reliably detect players and fast-moving sports balls across different scales and motion blur conditions.

**Tracker:** BoT-SORT
- **Reasoning:** BoT-SORT (Boost Track SORT) improves upon standard SORT and ByteTrack by incorporating camera motion compensation and a robust appearance feature extractor. In sports footage, rapid camera panning, zooming, and players crossing paths are common. BoT-SORT significantly reduces ID switching in these scenarios compared to purely intersection-over-union (IoU) based trackers.

## 2. Implemented Optional Enhancements

To further enrich the tracking pipeline, the following optional features were successfully integrated:
1. **Trajectory Visualization:** By maintaining a rolling queue (deque) of the past 30 center-point coordinates for each unique ID, the system renders a trailing polyline behind each player. This provides immediate visual context on player movement directions and speeds.
2. **Object Count Over Time:** A dynamic counter extracts the length of the active bounding box array in each frame, overlaying the live player/object count directly onto the video.

## 2.1 Web Application & Deployment

In addition to the core tracking pipeline, a full **Streamlit Web Application** (`app.py`) was developed and deployed on **Streamlit Community Cloud**, providing a public-facing interface for the project:
- Users can upload any sports video directly via the browser.
- A live progress bar displays the current frame being processed (e.g., "Processing frame 120 of 355").
- After processing, the annotated output video is displayed in the browser and available for download.
- The pipeline uses `imageio-ffmpeg` to automatically transcode the output to **H.264** for native browser playback.
- The app uses `opencv-python-headless` to ensure compatibility with Linux-based cloud servers that have no display (GUI) system.

## 3. Maintaining ID Consistency

ID consistency is maintained through a combination of spatial and appearance cues utilized by BoT-SORT:
1. **Kalman Filter & Motion Compensation:** Predicts the next location of an object. The camera motion compensation specifically helps when the background is shifting (panning camera).
2. **Appearance Embeddings (Re-ID):** Extracts visual features of the tracked objects. If a player is briefly occluded by another player, the tracker uses their visual appearance to re-assign the correct ID once they are visible again, rather than assigning a new ID.
3. **Low-Confidence Detections:** Similar to ByteTrack, BoT-SORT utilizes low-confidence detections to maintain tracks that are partially occluded, rather than discarding them.

## 4. Challenges Faced & Mitigations

- **Camera Motion:** Sports videos often feature erratic camera pans, which can confuse simple IoU trackers, causing them to lose the track or switch IDs. *Mitigated by BoT-SORT's global motion compensation.*
- **Occlusion:** Players bunching up (e.g., during a tackle or huddle) leads to missed detections and overlapping bounding boxes.
- **Similar Appearance:** Players on the same team wear identical uniforms, making appearance-based re-identification difficult if spatial cues fail.
- **Fast-Moving Objects (Motion Blur):** When a sports ball is kicked, its velocity increases significantly, causing motion blur. This lowers YOLO's detection confidence and drastically increases the distance the ball travels between frames, causing standard trackers to lose the ID. 
  - *Mitigation Implemented:* Created a `custom_botsort.yaml` configuration that lowers the detection confidence threshold (to 0.2), increases the `track_buffer` (to keep the track alive while the ball is a blurred streak), and increases the `match_thresh` to account for the larger frame-to-frame displacement.

## 5. Failure Cases Observed

- **Prolonged Occlusion:** If a player is hidden behind a group of players for an extended period, the tracker may eventually terminate their track and assign a new ID when they emerge.
- **Tiny Objects:** Even with custom tracking parameters, if the sports ball is extremely far away and very small, it might not be detected consistently unless using a heavier model variant (e.g., `yolov8x`).

## 6. Possible Improvements

1. **Fine-Tuning:** Fine-tune the YOLOv8 model on a specific sports dataset (e.g., a football tracking dataset) to improve detection accuracy on small objects and specific player poses.
2. **Team Clustering:** Implement an algorithm to extract the dominant color from each player's bounding box to automatically classify them into "Team A" or "Team B", adding valuable context to the tracker.
3. **Advanced Re-ID Models:** Replace the default feature extractor in BoT-SORT with a stronger, specialized Re-ID network trained explicitly on sports datasets.
4. **Trajectory Smoothing:** Apply post-processing (e.g., Gaussian smoothing) to the tracked coordinates to handle jitter in bounding boxes.
