import streamlit as st
import os
import tempfile
from tracker import VideoTracker

st.set_page_config(page_title="Multi-Object Tracking", layout="wide")

st.title("🏃‍♂️ Multi-Object Tracking & Trajectory Visualization")
st.write("Upload a sports video to process it with YOLOv8 and BoT-SORT in real-time.")

uploaded_file = st.file_uploader("Upload Video (MP4)", type=["mp4"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    input_path = tfile.name
    
    output_path = os.path.join(tempfile.gettempdir(), "tracked_output.mp4")

    if st.button("Start Processing"):
        tracker = VideoTracker()
        
        st.write("### Processing...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        # process_video is now a generator that yields (frame, total) for progress
        for current_frame, total_frames in tracker.process_video(input_path, output_path):
            pct = int((current_frame / total_frames) * 100)
            progress_bar.progress(pct)
            status_text.markdown(
                f"⚙️ **Processing frame {current_frame} of {total_frames}** &nbsp;|&nbsp; {pct}% complete"
            )

        progress_bar.progress(100)
        status_text.markdown("✅ **Processing complete!**")
        st.write("### Final Output")
        try:
            st.video(output_path)
        except Exception as e:
            st.warning("Could not play the video directly in the browser (Codec issue). Please download it below.")
        
        # Provide download button for the final video
        with open(output_path, "rb") as video_file:
            st.download_button(
                label="Download Tracked Video",
                data=video_file,
                file_name="tracked_output.mp4",
                mime="video/mp4"
            )
