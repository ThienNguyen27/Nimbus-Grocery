import os, glob

with open("data/classes.txt", "r") as f:
    names = [line.strip() for line in f if line.strip()]

REMOVE_CLASSES = ["Tomato", "Red-grapefruit", "Passion-Fruit", "Papaya"]
REMOVE_IDS = [names.index(c) for c in REMOVE_CLASSES if c in names]
print(f"Removing classes {REMOVE_CLASSES} at indices {REMOVE_IDS}")

# point to your two label dirs
LABEL_DIRS = ["data/labels/train", "data/labels/train"]

for labels_dir in LABEL_DIRS:
    pattern = os.path.join(labels_dir, "*.txt")
    for label_path in glob.glob(pattern):
        new_lines = []
        with open(label_path, "r") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    # skip blank or malformed lines
                    continue
                cls_id = int(parts[0])
                # drop unwanted
                if cls_id in REMOVE_IDS:
                    continue
                # shift down any higher IDs so there are no gaps
                shift = sum(1 for rid in REMOVE_IDS if cls_id > rid)
                parts[0] = str(cls_id - shift)
                new_lines.append(" ".join(parts))
        # overwrite with cleaned labels
        with open(label_path, "w") as f:
            f.write("\n".join(new_lines) + "\n")

print("✅ Labels cleaned in:", LABEL_DIRS)