import cv2
import os
from pathlib import Path

def extract_frames(video_path, output_folder, frame_rate=1):
    """Extracts frames from a video at a specified frame rate."""
    video_path = Path(video_path)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    video_name = video_path.stem
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return
        
    frame_count = 0
    saved_frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save a frame every 'frame_rate' seconds
        if frame_count % (int(cap.get(cv2.CAP_PROP_FPS)) // frame_rate) == 0:
            frame_filename = output_folder / f"{video_name}_frame_{saved_frame_count:04d}.jpg"
            cv2.imwrite(str(frame_filename), frame)
            saved_frame_count += 1
        
        frame_count += 1
        
    cap.release()
    print(f"Extracted {saved_frame_count} frames from {video_name}")

if __name__ == "__main__":
    RAW_VIDEOS_DIR = Path("../data/raw_videos")
    FRAMES_DIR = Path("../data/frames")
    
    for video_file in RAW_VIDEOS_DIR.glob("*.mp4"): # or .mov, etc.
        extract_frames(video_file, FRAMES_DIR, frame_rate=2) # Extract 2 frames per second