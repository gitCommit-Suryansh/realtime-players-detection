import streamlit as st
import os
import tempfile
import subprocess
from tracker import VideoTracker

st.set_page_config(page_title="Multi-Object Tracking", layout="wide")

st.title("🏃‍♂️ Multi-Object Tracking & Trajectory Visualization")
st.write("Upload a sports video to process it with YOLOv8 and BoT-SORT.")

# Use session state to remember the output path across button clicks
if "output_path" not in st.session_state:
    st.session_state.output_path = None

uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    input_path = tfile.name
    raw_output_path = os.path.join(tempfile.gettempdir(), "tracked_output.mp4")

    if st.button("▶️ Start Processing"):
        tracker = VideoTracker()
        
        st.write("### ⚙️ Processing...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        for current_frame, total_frames in tracker.process_video(input_path, raw_output_path):
            pct = int((current_frame / total_frames) * 100)
            progress_bar.progress(pct)
            status_text.markdown(
                f"⚙️ **Processing frame {current_frame} of {total_frames}** &nbsp;|&nbsp; {pct}% complete"
            )

        progress_bar.progress(100)
        status_text.markdown("✅ **Done! Converting video for browser playback...**")

        # Convert to H.264 for browser playback using imageio-ffmpeg
        web_output = raw_output_path.replace(".mp4", "_web.mp4")
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            subprocess.run([
                ffmpeg_path, '-y', '-i', raw_output_path,
                '-vcodec', 'libx264', '-preset', 'fast',
                '-pix_fmt', 'yuv420p', web_output
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(web_output) and os.path.getsize(web_output) > 0:
                st.session_state.output_path = web_output
            else:
                st.session_state.output_path = raw_output_path
        except Exception as e:
            print(f"FFMPEG conversion failed: {e}")
            st.session_state.output_path = raw_output_path

        status_text.markdown("✅ **Processing complete!**")
        st.rerun()

    # Show result if we already have a processed video (persists across button clicks)
    if st.session_state.output_path and os.path.exists(st.session_state.output_path):
        st.write("### 🎬 Final Output")
        try:
            with open(st.session_state.output_path, "rb") as f:
                video_bytes = f.read()
            st.video(video_bytes)
        except Exception as e:
            st.warning("Video could not be previewed in browser. Please download it below.")

        with open(st.session_state.output_path, "rb") as video_file:
            st.download_button(
                label="⬇️ Download Tracked Video",
                data=video_file,
                file_name="tracked_output.mp4",
                mime="video/mp4"
            )

        if st.button("🔄 Reload Video"):
            st.rerun()
