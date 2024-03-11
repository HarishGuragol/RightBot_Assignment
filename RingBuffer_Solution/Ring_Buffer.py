import cv2
import threading
import time
import os
import sys

class RingBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = [None] * capacity
        self.index = 0

    def append(self, item):
        self.buffer[self.index] = item
        self.index = (self.index + 1) % self.capacity

    def get(self):
        return [item for item in self.buffer if item is not None]

def producer(buffer, video_capture, total_frames, producer_frame_count):
    frame_count = 0
    while frame_count < total_frames:
        ret, frame = video_capture.read()
        if ret:
            buffer.append(frame)
            print("Produced frame")
            frame_count += 1
            producer_frame_count.append(frame_count)  # Update producer frame count
        else:
            print("Failed to capture frame")
        time.sleep(0.1)  # Adjust this delay as per your requirement

def consumer(buffer, save_dir, consumer_frame_count):
    frame_count = 0
    while True:
        frames = buffer.get()
        if frames:
            for frame in frames:
                cv2.imshow("Live Video", frame)
                cv2.waitKey(1)  # Adjust the delay between frames as needed
                frame_count += 1
                consumer_frame_count.append(frame_count)  # Update consumer frame count
                cv2.imwrite(os.path.join(save_dir, f"frame_{frame_count}.jpg"), frame)
                if frame_count >= 500:
                    print("consumer_data", len(consumer_frame_count))
                    print("Reached 500 frames. Terminating...")
                    cv2.destroyAllWindows()  # Close OpenCV windows
                    sys.exit()  # Exit the program
            print("Consumed frames")
        else:
            print("Buffer is empty")
            time.sleep(0.1)  # Adjust this delay if the buffer is constantly empty

def main():
    buffer_capacity = 10  # Adjust the buffer capacity as needed
    ring_buffer = RingBuffer(buffer_capacity)
    video_capture = cv2.VideoCapture(0)  # Adjust the camera index as needed

    save_dir = "captured_frames_data"
    os.makedirs(save_dir, exist_ok=True)

    producer_frame_count = []  # Track number of frames produced
    consumer_frame_count = []  # Track number of frames consumed

    producer_thread = threading.Thread(target=producer, args=(ring_buffer, video_capture, 500, producer_frame_count))
    consumer_thread = threading.Thread(target=consumer, args=(ring_buffer, save_dir, consumer_frame_count))

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    consumer_thread.join()

    video_capture.release()

    print("Total frames produced:", len(producer_frame_count))
    print("Total frames consumed:", len(consumer_frame_count))

if __name__ == "__main__":
    main()
