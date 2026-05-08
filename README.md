# Multi-Object Detection and Persistent ID Tracking

This project implements a computer vision pipeline capable of detecting and tracking multiple subjects (e.g., players, athletes, and sports balls) in public sports/event footage.

## Features
- **Interactive Web App:** Upload any sports video via the Streamlit web interface and get the tracked video processed directly in your browser.
- **Object Detection:** Detects `person` and `sports ball` in every frame using YOLOv8m.
- **Multi-Object Tracking:** Uses BoT-SORT to assign unique and persistent IDs across the full video duration.
- **Robustness:** BoT-SORT handles occlusion, scale changes, and camera motion — essential for sports footage.
- **Trajectory Visualization:** Draws a trailing yellow path behind each tracked object to visualize movement patterns over time.
- **Active Object Count:** Dynamically overlays the live count of tracked subjects on every frame.
- **Live Progress Bar:** The web UI displays a real-time frame-by-frame progress indicator while processing.
- **Download Output:** Download the fully annotated output video directly from the web app.

## Mandatory Deliverables

- **Original Video Link:** [Vecteezy - Football Players Kicking The Ball](https://www.vecteezy.com/video/28545534-football-players-kicking-the-ball-on-pre-game-train)
- **Technical Report:** Available in [`Technical_Report.md`](Technical_Report.md).
- **Annotated Output Video:** Available in the `output/` directory.
- **Demo Video:** [Watch Demo on Google Drive](https://drive.google.com/file/d/1o49Usb3Uhtqc3pUN64_AGkqWX39Asrj3/view?usp=sharing)

## Sample Screenshots

Below are sample screenshots demonstrating the YOLOv8 detections, BoT-SORT persistent IDs, object count, and trajectory visualizations:

![Screenshot 1](attachments/Screenshot%202026-05-08%20110750.png)
![Screenshot 2](attachments/Screenshot%202026-05-08%20111517.png)
![Screenshot 3](attachments/Screenshot%202026-05-08%20111532.png)
![Screenshot 4](attachments/Screenshot%202026-05-08%20111547.png)

## Installation

1. Clone this repository.
2. Ensure you have Python 3.8+ installed.
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
4. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### ✅ Primary: Streamlit Web App (Recommended)
The easiest way to use this project. Upload a video and get the tracked result directly in your browser:
```bash
python -m streamlit run app.py
```
Then open [http://localhost:8501](http://localhost:8501), upload your sports video, click **"▶️ Start Processing"**, and download the result.

### Live Deployment
This app is also deployed publicly on **Streamlit Community Cloud** and can be accessed directly via the live URL without any local setup.

### Alternative: Command Line Interface
For headless/server-side processing without the UI:
1. Place your input video inside the `data/` folder.
2. Run:
   ```bash
   python main.py --video your_video.mp4
   ```
3. The annotated video will be saved in the `output/` folder.

## Configuration
You can modify `config.py` to tune the pipeline:
- `MODEL_NAME` — Switch YOLO model variant (e.g., `yolov8n.pt` for fastest speed, `yolov8m.pt` for best accuracy).
- `TARGET_CLASSES` — Change which COCO object classes to track (e.g., add class `2` for cars).
- `CONFIDENCE_THRESHOLD` — Lower this to detect more objects; raise it to reduce false positives.
- `IMGSZ` — Reduce inference resolution (e.g., `320`) for faster processing on slow hardware.
- `FRAME_SKIP` — Process every Nth frame to significantly speed up processing.

## Project Structure
```
├── app.py                # Streamlit Web Application (primary interface)
├── tracker.py            # Core YOLOv8 + BoT-SORT tracking logic
├── config.py             # All configuration parameters
├── main.py               # Command-line interface script
├── custom_botsort.yaml   # Custom BoT-SORT configuration for sports footage
├── requirements.txt      # Python dependencies
├── packages.txt          # System dependencies for cloud deployment
├── Technical_Report.md   # Detailed technical report
└── Attachments/          # Sample output screenshots
```

## Assumptions & Limitations
- **Assumptions:**
  - Subjects to be tracked fall into standard COCO dataset classes (people, sports balls).
  - The Streamlit app processes videos sequentially (one at a time).
- **Limitations:**
  - Processing speed depends on hardware. A GPU significantly accelerates inference.
  - Severe occlusions or completely overlapping subjects of identical appearance may still cause ID switches.
  - Very small or fast-moving objects (like a distant sports ball mid-kick) may not be detected consistently on every frame.
