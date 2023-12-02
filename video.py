import cv2
import numpy as np
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def process_frame(frame):
    # Convert frame to RGB (OpenCV uses BGR by default)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Create a mask where black pixels ([0,0,0]) are detected in the frame
    mask = cv2.inRange(frame_rgb, (0,0,0), (10,10,10))

    # Invert mask to get parts that are not black
    mask_inv = cv2.bitwise_not(mask)

    # Use the mask to extract the facecam area (excluding black background)
    facecam_area = cv2.bitwise_and(frame_rgb, frame_rgb, mask=mask_inv)

    # Resize screenshot to frame size
    resized_screenshot = cv2.resize(screenshot, (frame.shape[1], frame.shape[0]))

    # Combine the facecam area and the resized screenshot
    combined = cv2.bitwise_and(resized_screenshot, resized_screenshot, mask=mask)
    combined = cv2.add(combined, facecam_area)

    # Convert back to BGR for MoviePy
    final_frame = cv2.cvtColor(combined, cv2.COLOR_RGB2BGR)
    return final_frame

# Load your screenshot and facecam video
screenshot = cv2.imread("screenshots/bolt.com.png")
facecam_video = VideoFileClip("video.mp4")

# Apply the processing to each frame
processed_video = facecam_video.fl_image(process_frame)

# Write the result to a file
processed_video.write_videofile("output_video.mp4", fps=facecam_video.fps)
