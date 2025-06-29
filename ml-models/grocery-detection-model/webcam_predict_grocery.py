import cv2
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import numpy as np
import pandas as pd

# === SETUP ===
# Load class ID to coarse class mapping
class_df = pd.read_csv("classes.csv")
id_to_coarse = dict(zip(class_df["Class ID (int)"], class_df["Coarse Class Name (str)"]))
all_class_ids = sorted(class_df["Class ID (int)"].unique())
class_id_to_index = {cid: idx for idx, cid in enumerate(all_class_ids)}
index_to_class_id = {v: k for k, v in class_id_to_index.items()}

# Load model
num_classes = len(index_to_class_id)
model = models.resnet18(pretrained=False)
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
model.load_state_dict(torch.load("grocery_model.pt", map_location=torch.device('cpu')))
model.eval()

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# === WEBCAM LOOP ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess frame
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    input_tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(input_tensor)
        pred_idx = output.argmax(1).item()
        pred_class_id = index_to_class_id[pred_idx]
        coarse_name = id_to_coarse[pred_class_id]

    # Draw prediction
    cv2.rectangle(frame, (50, 50), (300, 300), (0, 255, 0), 2)
    cv2.putText(frame, coarse_name, (55, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show webcam
    cv2.imshow("Grocery Classifier", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
