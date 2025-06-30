# test_yolov8.py

from ultralytics import YOLO
import cv2

# Path to your fine-tuned weights
MODEL_PATH = "run/train/grocery_finetune5/weights/best.pt"

# Load the model once
model = YOLO(MODEL_PATH)

def preprocess_frame(frame, blur_background=True):
    h, w, _ = frame.shape
    center_x, center_y = w // 2, h // 2

    # Define crop box (center 60% of frame)
    crop_w, crop_h = int(w * 0.6), int(h * 0.6)
    x1, y1 = center_x - crop_w // 2, center_y - crop_h // 2
    x2, y2 = center_x + crop_w // 2, center_y + crop_h // 2

    cropped = frame[y1:y2, x1:x2].copy()

    if blur_background:
        # Blur entire frame
        blurred = cv2.GaussianBlur(frame, (45, 45), 0)
        # Restore central region
        blurred[y1:y2, x1:x2] = cropped
        output = blurred
    else:
        output = cropped

    # Draw border around center box (visible ROI)
    border_color = (255, 255, 255)  # White
    border_thickness = 2
    cv2.rectangle(output, (x1, y1), (x2, y2), border_color, border_thickness)

    return output
    
def run_model_on_file(file_path: str, conf: float = 0.25, iou: float = 0.45):
    """
    Run the YOLOv8 model on a single image or video file.

    Args:
        file_path (str): Path to the image or video file.
        conf (float): Confidence threshold for detections.
        iou (float): IoU threshold for non-max suppression.
    """
    results = model.predict(
        source=file_path,
        conf=conf,
        iou=iou,
        save=False,       
        show=False       
    )

    frame = results[0].plot()
    # Display and wait for any key
    cv2.imshow("YOLOv8 Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def run_model_on_webcam(conf: float = 0.25, iou: float = 0.45, cam_index: int = 0):
    """
    Run the YOLOv8 model on webcam feed.

    Args:
        conf (float): Confidence threshold for detections.
        iou (float): IoU threshold for non-max suppression.
        cam_index (int): OpenCV camera index (0, 1, ...).
    """

    cap = cv2.VideoCapture(cam_index)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply preprocessing
        processed_frame = preprocess_frame(frame, blur_background=True)

        # Run detection
        results = model.predict(processed_frame, conf=conf, iou=iou, verbose=False)

        # Show result
        annotated = results[0].plot()
        cv2.imshow("YOLOv8 Preprocessed Detection", annotated)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # To test on a file, uncomment below and set the correct path:
    # run_model_on_file("imagesToTest/manHoldingApple.jpg")

    # run_model_on_webcam()
    
    # If both are commented, nothing will run. Just choose one!
    pass
