import os
from moviepy import VideoFileClip
import speech_recognition as sr
import streamlit as st

def extract_audio_from_video(video_file, output_audio="temp_audio.wav"):
    """
    Extracts audio from a video file and saves it as a WAV file.
    
    Args:
        video_file (str): Path to the input video file (e.g., 'response_q1.avi').
        output_audio (str): Path to save the output WAV file.
    
    Returns:
        str: Path to the extracted audio file, or None if failed.
    """
    try:
        # Load the video file
        video = VideoFileClip(video_file)
        # Extract audio
        audio = video.audio
        # Save audio as WAV
        audio.write_audiofile(output_audio, codec='pcm_s16le')
        # Close files to free resources
        audio.close()
        video.close()
        return output_audio if os.path.exists(output_audio) else None
    except Exception as e:
        st.error(f"Error extracting audio from {video_file}: {str(e)}")
        return None

def transcribe_audio(audio_file):
    """
    Transcribes audio to text using Google's Speech-to-Text API.
    
    Args:
        audio_file (str): Path to the input WAV audio file.
    
    Returns:
        str: Transcribed text, or error message if failed.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return "Could not understand audio."
    except sr.RequestError as e:
        return f"Speech recognition error: {str(e)}"
    except Exception as e:
        return f"Transcription error: {str(e)}"

def process_videos(video_files):
    """
    Processes a list of video files to extract audio and transcribe to text.
    
    Args:
        video_files (list): List of video file paths.
    
    Returns:
        list: List of transcribed texts (or error messages) for each video.
    """
    transcriptions = []
    for i, video_file in enumerate(video_files):
        if not os.path.exists(video_file):
            transcriptions.append(f"Video file {video_file} not found.")
            continue
        
        # Extract audio
        audio_file = f"temp_audio_q{i + 1}.wav"
        extracted_audio = extract_audio_from_video(video_file, audio_file)
        if extracted_audio:
            # Transcribe audio
            text = transcribe_audio(extracted_audio)
            transcriptions.append(text)
            # Clean up temporary audio file
            if os.path.exists(audio_file):
                os.remove(audio_file)
        else:
            transcriptions.append(f"Failed to extract audio from {video_file}.")
    
    return transcriptions

# Streamlit app for testing
st.title("Extract Audio and Transcribe Videos")

# Initialize session state
if "video_files" not in st.session_state:
    st.session_state.video_files = []

# Allow manual upload for testing (replace with livetest.py integration later)
uploaded_files = st.file_uploader("Upload video files (for testing)", accept_multiple_files=True, type=["avi", "mp4"])
if uploaded_files:
    st.session_state.video_files = []
    for uploaded_file in uploaded_files:
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state.video_files.append(uploaded_file.name)

# Process videos when button is clicked
if st.button("Process Videos") and st.session_state.video_files:
    st.write("Processing videos...")
    transcriptions = process_videos(st.session_state.video_files)
    
    # Display results
    st.subheader("Transcriptions")
    for i, text in enumerate(transcriptions):
        st.write(f"Question {i + 1}: {text}")
    
    # Store transcriptions in session state for later use
    if "module_conclusions" not in st.session_state:
        st.session_state.module_conclusions = {}
    st.session_state.module_conclusions["iq_eq_test"] = {
        "transcriptions": transcriptions,
        "conclusion": "Pending LLM analysis of transcriptions",
        "suggested_domains": ["TBD"]
    }
    st.subheader("Stored Module Conclusions")
    st.json(st.session_state.module_conclusions)

# Instructions
st.write("Upload video files or integrate with livetest.py to process IQ/EQ test responses. Click 'Process Videos' to extract audio and transcribe.")