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
            frame_count += 1
            producer_frame_count.append(frame_count)  
        else:
            print("Failed to capture frame")
        time.sleep(0.1)

def consumer(buffer, save_dir, consumer_frame_count):
    frame_count = 0
    while True:
        frames = buffer.get()
        if frames:
            for frame in frames:
                cv2.imshow("Live Video", frame)
                cv2.waitKey(1)  
                frame_count += 1
                consumer_frame_count.append(frame_count)  
                cv2.imwrite(os.path.join(save_dir, f"frame_{frame_count}.jpg"), frame)
                if frame_count >= 500:
                    cv2.destroyAllWindows() 
                    sys.exit()  
        else:
            time.sleep(0.1)

def main():
    buffer_capacity = 10  
    ring_buffer = RingBuffer(buffer_capacity)
    video_capture = cv2.VideoCapture(0)  

    save_dir = "captured_frames_data"
    os.makedirs(save_dir, exist_ok=True)

    producer_frame_count = [] 
    consumer_frame_count = []  

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
