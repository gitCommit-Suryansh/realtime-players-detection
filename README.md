# Multi-Object Detection and Persistent ID Tracking

This project implements a computer vision pipeline capable of detecting and tracking multiple subjects (e.g., players, athletes, and sports balls) in public sports/event footage.

## Features
- **Object Detection:** Detects `person` and `sports ball` using YOLOv8.
- **Multi-Object Tracking:** Uses BoT-SORT to assign unique and persistent IDs to detected subjects.
- **Robustness:** BoT-SORT helps handle occlusion, scale changes, and camera motion, making it highly suitable for sports footage.
- **Trajectory Visualization:** Draws a trailing yellow path behind each tracked object to visualize movement patterns over time.
- **Active Object Count:** Dynamically calculates and displays the total number of currently tracked subjects on the screen.
- **Video Annotation:** Generates an output video with bounding boxes, tracked IDs, paths, and metadata.

## Mandatory Deliverables

- **Original Video Link:** [Vecteezy - Football Players Kicking The Ball](https://www.vecteezy.com/video/28545534-football-players-kicking-the-ball-on-pre-game-train)
- **Technical Report:** Available in [`Technical_Report.md`](Technical_Report.md).
- **Annotated Output Video:** Available in the `output/` directory.
- **Demo Video:** [Watch Demo on Google Drive](https://drive.google.com/file/d/1calNJQzUBFSmXqbUfy7Xss2Bz6Rs9Goh/view?usp=sharing)

## Sample Screenshots

Below are sample screenshots demonstrating the YOLOv8 detections, BoT-SORT persistent IDs, object count, and trajectory visualizations:

![Screenshot 1](attachments/Screenshot%202026-05-08%20110750.png)
![Screenshot 2](attachments/Screenshot%202026-05-08%20111517.png)
![Screenshot 3](attachments/Screenshot%202026-05-08%20111532.png)
![Screenshot 4](attachments/Screenshot%202026-05-08%20111547.png)

## Installation

1. Clone or download this repository.
2. Ensure you have Python 3.8+ installed.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

There are two ways to run this pipeline: via the Command Line Interface (CLI) or the live Web App (Streamlit).

### 1. Web App Interface (Live Processing)
To launch the beautiful, interactive web UI where you can upload videos and watch the YOLO detections happen in real-time:
```bash
streamlit run app.py
```

### 2. Command Line Interface (Headless)
1. Place your input video inside the `data/` folder.
2. Run the tracking pipeline by executing:
   ```bash
   python main.py --video your_video.mp4
   ```
3. The processed video with annotations will be saved in the `output/` folder.

## Configuration
You can modify `config.py` to:
- Change the target classes (e.g., track vehicles instead of people by adding COCO class `2` to `TARGET_CLASSES`).
- Adjust the `CONFIDENCE_THRESHOLD`.
- Swap the tracker from `botsort.yaml` to `bytetrack.yaml`.

## Assumptions & Limitations
- **Assumptions:** 
  - The subjects to be tracked fall into standard COCO dataset classes (people, sports balls).
  - The video resolution and FPS are reasonable enough to be processed on local hardware.
- **Limitations:**
  - Severe occlusions or completely overlapping subjects of identical appearance might still cause ID switches.
  - Very small objects (like a distant sports ball) might not be detected consistently unless using a larger YOLO model (e.g., `yolov8x`).
