import os
import argparse
from tracker import VideoTracker
from config import INPUT_DIR, OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Object Detection and Tracking Pipeline"
    )
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Name of the video file in the 'data' folder, or full path to video.",
    )
    args = parser.parse_args()

    video_path = args.video

    if not os.path.exists(video_path):
        video_path = os.path.join(INPUT_DIR, args.video)

    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        print(
            f"Please ensure your video is placed in the '{INPUT_DIR}' directory or provide a full absolute path."
        )
        return

    filename = os.path.basename(video_path)
    output_path = os.path.join(OUTPUT_DIR, f"tracked_{filename}")

    # Initialize tracker and process video
    tracker = VideoTracker()
    tracker.process_video(video_path, output_path)


if __name__ == "__main__":
    main()
