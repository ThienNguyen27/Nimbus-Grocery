
# 1. Read your classes.txt
with open("data/classes.txt", "r") as f:
    names = [line.strip() for line in f if line.strip()]

# 2. Print all class names with their indices
print("All classes and their indices:")
for idx, name in enumerate(names):
    print(f"{idx}: {name}")

# 3. Lookup unwanted classes
unwanted = ["Tomato", "Red-grapefruit"]
print("\nIndices for unwanted classes:")
for c in unwanted:
    if c in names:
        print(f"{c} → {names.index(c)}")
    else:
        print(f"{c} not found in classes.txt")