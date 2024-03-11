# Video Processing with OpenCV

This repository contains a Python script for real-time video processing using OpenCV. The script captures video from a webcam, identifies nested rectangles in the frames, calculates their levels, and saves frames with levels 2 or 3 in corresponding folders. Additionally, it saves the processed video as an MP4 file.

## Dependencies

- Python 3.x
- OpenCV (cv2)

## Usage

1. Clone this repository to your local machine.
2. Run the script Recangle.py`.
3. The script will capture video from your webcam and process it in real-time.
4. Frames with nested rectangles of levels 2 or 3 will be saved in the 'output_frames' folder, while the processed video will be saved as 'output.mp4'.
5. The script will automatically stop after processing 2000 frames.

## Files

- `video_processing.py`: Python script for real-time video processing.
- `output.mp4`: Processed video saved in MP4 format.
- `output_frames/`: Folder containing frames with nested rectangles of levels 2 or 3, organized in subfolders 'level2' and 'level3' respectively.

## License

This project is licensed under the [MIT License](LICENSE).
