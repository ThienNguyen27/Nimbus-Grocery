import yaml


# Sanity Check
with open('data.yaml') as f:
    cfg = yaml.safe_load(f)
print(cfg)
