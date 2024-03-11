import cv2
import os

# Function to calculate the level of nested rectangles
def calculate_level(outer_rectangles):
    level = 1
    for i, outer_rect in enumerate(outer_rectangles):
        for j, compare_rect in enumerate(outer_rectangles):
            if i != j and is_inside(outer_rect, compare_rect):
                level += 1
                break
    return level

# Function to check if one rectangle is inside another
def is_inside(outer_rect, inner_rect):
    x1, y1, w1, h1 = outer_rect
    x2, y2, w2, h2 = inner_rect

    return x2 >= x1 and y2 >= y1 and x2 + w2 <= x1 + w1 and y2 + h2 <= y1 + h1

# Capture live video from webcam
cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (640, 480))

# Counter for saved frames
frame_counter = 0

# Create directories for saving frames
output_folder = 'output_frames'
level2_folder = os.path.join(output_folder, 'level2')
level3_folder = os.path.join(output_folder, 'level3')
os.makedirs(level2_folder, exist_ok=True)
os.makedirs(level3_folder, exist_ok=True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_counter += 1

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    outer_rectangles = []
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # If the contour has four corners, it's likely a rectangle
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            outer_rectangles.append((x, y, w, h))

    # Calculate level of nested rectangles
    level = calculate_level(outer_rectangles)

    # Draw outermost rectangles, highlight them, and put text for location
    for i, rect in enumerate(outer_rectangles):
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, f'{i+1}: ({x}, {y})', (int(x + w / 2), int(y + h / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Write level on the frame
    cv2.putText(frame, f'Level: {level}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Save frames with level 2 or 3 in corresponding folders
    if level == 2:
        filename = f'frame_level_{level}_{frame_counter}.jpg'
        filepath = os.path.join(level2_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Level {level} frame saved: {filepath}")
    elif level == 3:
        filename = f'frame_level_{level}_{frame_counter}.jpg'
        filepath = os.path.join(level3_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"Level {level} frame saved: {filepath}")

    # Write the frame to the output video
    out.write(frame)

    if frame_counter >= 2000:
        print("Reached 2000 frames. Saving video and exiting...")
        break

# Release the capture and writer
cap.release()
out.release()
cv2.destroyAllWindows()
