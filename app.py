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

    st.write("### Live Processing Feed")
    # Placeholder for the live video stream
    stframe = st.empty()
    
    if st.button("Start Processing"):
        tracker = VideoTracker()
        
        with st.spinner("Processing video..."):
            # Stream the frames live
            for frame in tracker.process_video_stream(input_path, output_path):
                # use_container_width is the modern equivalent of use_column_width
                stframe.image(frame, channels="RGB", use_container_width=True)
                
        st.success("Processing Complete!")
        
        # Provide download button for the final video
        with open(output_path, "rb") as video_file:
            st.download_button(
                label="Download Tracked Video",
                data=video_file,
                file_name="tracked_output.mp4",
                mime="video/mp4"
            )
