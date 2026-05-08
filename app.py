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
        
        with st.spinner("Processing video... This may take a few minutes."):
            # Process the video completely in the background
            tracker.process_video(input_path, output_path)
            
            # --- FFMPEG CONVERSION FOR BROWSER PLAYBACK ---
            try:
                import imageio_ffmpeg
                import subprocess
                
                web_output_path = output_path.replace('.mp4', '_web.mp4')
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                
                # Run ffmpeg to convert mp4v to H.264 (avc1) for native browser playback
                subprocess.run([
                    ffmpeg_path, '-y', '-i', output_path, 
                    '-vcodec', 'libx264', '-preset', 'fast', web_output_path
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # If successful, use the web-compatible video for display and download
                if os.path.exists(web_output_path):
                    output_path = web_output_path
            except Exception as e:
                print(f"FFMPEG conversion failed: {e}")
            # ----------------------------------------------
                
        st.success("Processing Complete!")
        st.balloons()
        
        # Display the final video on the screen
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
