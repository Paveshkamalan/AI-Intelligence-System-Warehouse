import cv2
import os


def read_video(video_path):
    if not os.path.exists(video_path):
        print(f"Error: Video not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    print("================================")
    print("VIDEO INFORMATION")
    print("================================")
    print(f"Video: {video_path}")
    print(f"FPS: {fps}")
    print(f"Resolution: {width}x{height}")
    print(f"Frames: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    print("================================")

    cap.release()


if __name__ == "__main__":
    video_path = "data/raw/warehouse_demo.mp4"
    read_video(video_path)