from os import listdir
from PIL import Image
from pathlib import Path

for filename in Path('./datasets/rsna-pneumonia-detection-challenge-jpeg/train_augmented').glob("**/*.JPEG"):
    try:
        img = Image.open('./' + str(filename))  # open the image file
        img.verify()  # verify that it is, in fact an image
    except (IOError, SyntaxError) as e:
        print('Bad file:', filename)
        filename.unlink()
