import os, shutil, random

img_dir = 'images'
lbl_dir = 'labels'

imgs = [f for f in os.listdir(img_dir) if f.lower().endswith(('.jpg','.png','.jpeg'))]
random.shuffle(imgs)
split = int(0.8 * len(imgs))
train_imgs, test_imgs = imgs[:split], imgs[split:]

for subset, files in [('train', train_imgs), ('test', test_imgs)]:
    os.makedirs(f'{img_dir}/{subset}', exist_ok=True)
    os.makedirs(f'{lbl_dir}/{subset}', exist_ok=True)
    for img in files:
        base = os.path.splitext(img)[0]
        shutil.move(f'{img_dir}/{img}', f'{img_dir}/{subset}/{img}')
        shutil.move(f'{lbl_dir}/{base}.txt', f'{lbl_dir}/{subset}/{base}.txt')