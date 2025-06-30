# test_yolov8.py

from ultralytics import YOLO
import cv2

# Path to your fine-tuned weights
MODEL_PATH = "run/train/grocery_finetune5/weights/best.pt"

# Load the model once
model = YOLO(MODEL_PATH)

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
    results = model.predict(
        source=cam_index,
        conf=conf,
        iou=iou,
        show=True        # opens webcam window with detections
    )
    # Note: this will run until you close the window (e.g., press 'q' in the OpenCV window).

if __name__ == "__main__":
    # To test on a file, uncomment below and set the correct path:
    run_model_on_file("imagesToTest/manHoldingApple.jpg")

    # To test on your webcam, uncomment below:
    # run_model_on_webcam()
    
    # If both are commented, nothing will run. Just choose one!
    pass
