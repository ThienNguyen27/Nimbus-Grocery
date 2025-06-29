import face_recognition
import cv2
import numpy as np
import sys
import os

def load_known_faces():
    """Load and encode known faces from the dataset."""
    try:
        BaoPhuc_image = face_recognition.load_image_file("Dataset/BaoPhuc.jpeg")
        BaoPhuc_face_encoding = face_recognition.face_encodings(BaoPhuc_image)[0]

        ChiThien_image = face_recognition.load_image_file("Dataset/ChiThien.jpeg")
        ChiThien_face_encoding = face_recognition.face_encodings(ChiThien_image)[0]

        MinhThien_image = face_recognition.load_image_file("Dataset/MinhThien.png")
        MinhThien_face_encoding = face_recognition.face_encodings(MinhThien_image)[0]

        known_face_encodings = [BaoPhuc_face_encoding, ChiThien_face_encoding, MinhThien_face_encoding]
        known_face_names = ["Ryan Do", "Promaster", "MinhThien"]
        return known_face_encodings, known_face_names
    except (FileNotFoundError, IndexError) as e:
        print(f"Error loading reference images: {e}")
        return [], []

def safe_face_encodings(image, face_locations):
    """Safely get face encodings with error handling"""
    try:
        # Ensure image is in the right format
        if image.dtype != np.uint8:
            image = image.astype(np.uint8)
        
        # Ensure array is contiguous
        if not image.flags['C_CONTIGUOUS']:
            image = np.ascontiguousarray(image)
        
        return face_recognition.face_encodings(image, face_locations)
    except Exception as e:
        print(f"Error in face encoding: {e}")
        return []

def detect_person_image(image_path, known_face_encodings, known_face_names):
    """Detect faces, draw on the real original image (BGR), show it, and return best recognized name."""
    try:
        # Load image in original BGR format for display/drawing
        bgr_image = cv2.imread(image_path)

        if bgr_image is None:
            print(f"Failed to load image: {image_path}")
            return "Error"

        # Convert BGR to RGB for face_recognition (it expects RGB)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        rgb_image = np.ascontiguousarray(rgb_image, dtype=np.uint8)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = safe_face_encodings(rgb_image, face_locations)

        if not face_encodings:
            cv2.imshow(f"No face found: {os.path.basename(image_path)}", bgr_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return "No face found"

        best_name = "Unknown"

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            if True in matches:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if best_name == "Unknown":
                        best_name = name

            # Draw on the original BGR image
            cv2.rectangle(bgr_image, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(bgr_image, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(bgr_image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Show the real image (unaltered except for boxes/text)
        cv2.imshow(f"Detected: {best_name}", bgr_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return best_name

    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "Error"


def detect_person_realtime(known_face_encodings, known_face_names):
    """Detect faces in real-time from webcam and identify known persons."""
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("Error: Could not open webcam")
        return

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Could not read frame")
            break

        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            rgb_small_frame = np.ascontiguousarray(rgb_small_frame, dtype=np.uint8)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = safe_face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

def test_image():
    known_face_encodings, known_face_names = load_known_faces()
    if not known_face_encodings:
        print("No known faces loaded.")
        return []

    base_folder = "Test"
    test_files = [
        'testbp1.png', 'testbp2.png', 'testbp3.png',
        'testct1.jpeg', 'testct2.png', 'testct3.jpeg', 'testct4.jpeg',
        'testmt1.png', 'testmt2.png', 'testmt3.png', 'testmt4.png'
    ]

    results = []

    for fname in test_files:
        image_path = os.path.join(base_folder, fname)
        name = detect_person_image(image_path, known_face_encodings, known_face_names)
        results.append({
            "image": image_path,
            "recognized": name
        })

    for entry in results:
        print(f"Path: {entry['image']} -> Detected: {entry['recognized']}")

    return results


def test_camera():
    known_face_encodings, known_face_names = load_known_faces()
    if not known_face_encodings:
        print("No known faces loaded.")
        return

    detect_person_realtime(known_face_encodings, known_face_names)


def main():
    # Test with one image
    # test_image()

    # Test realtime
    test_camera()

if __name__ == "__main__":
    main()