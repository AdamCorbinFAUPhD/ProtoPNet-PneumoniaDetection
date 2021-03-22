# Because the origional dataset is so large we will create a smaller dataset.
from pathlib import Path
import shutil

dataset_sub_folder = Path("datasets/rsna-pneumonia-detection-challenge-jpeg-small_set")
test = dataset_sub_folder / "test"
train = dataset_sub_folder / "train"
train_aug = dataset_sub_folder / "train_augmented"

test_detected = test / "detected"
train_detected = train / "detected"

test_free = test / "free"
train_free = train / "free"

train_aug_free = train_aug / "free"
train_aug_detected = train_aug / "detected"





# Create all the folders
if not dataset_sub_folder.exists():
    dataset_sub_folder.mkdir()

if not test.exists():
    test.mkdir()

if not test_free.exists():
    test_free.mkdir()
if not test_detected.exists():
    test_detected.mkdir()

if not train.exists():
    train.mkdir()

if not train_detected.exists():
    train_detected.mkdir()

if not train_free.exists():
    train_free.mkdir()

if not train_aug.exists():
    train_aug.mkdir()
if not train_aug_free.exists():
    train_aug_free.mkdir()
if not train_aug_detected.exists():
    train_aug_detected.mkdir()
# Copy over files into the specific folders

full_dataset = Path("datasets/rsna-pneumonia-detection-challenge-jpeg")
full_dataset_test_detected = full_dataset / "test/detected"
full_dataset_test_free = full_dataset / "test/free"

full_dataset_train_detected = full_dataset / "train/detected"
full_dataset_train_free = full_dataset / "train/free"

full_dataset_train_aug_detected = full_dataset / "train_augmented/detected"
full_dataset_train_aug_free = full_dataset / "train_augmented/free"

folders_to_copy_files = [[full_dataset_test_detected, test_detected], [full_dataset_test_free, test_free],
                         [full_dataset_train_detected, train_detected], [full_dataset_train_free, train_free],
                         ]
for folders in folders_to_copy_files:
    full_folder = folders[0]
    subset_folder = folders[1]
    count = 0
    for f in full_folder.glob("**/*.*"):
        count += 1
    print(f"{full_folder} count: {count}")
    sub_percent = int(count * .1)
    count = 0
    for f in full_folder.glob("**/*.*"):
        # copy over image to sub_set area

        shutil.copy(f, str(subset_folder.absolute())+"/"+f.name)

        count += 1
        if count >= sub_percent:
            break
    print(f"Coppied over {sub_percent} images to {subset_folder}")

# It takes a long time to count the files in Aug so we will only copy the first 1k in each

aug_folders_to_copy_from = [[full_dataset_train_aug_detected, train_aug_detected], [full_dataset_train_aug_free, train_aug_free]]
for folders in aug_folders_to_copy_from:
    full_folder = folders[0]
    subset_folder = folders[1]

    sub_percent = 1000
    count = 0
    for f in full_folder.glob("**/*.*"):
        # copy over image to sub_set area
        shutil.copy(f, str(subset_folder.absolute())+"/"+f.name)
        count += 1
        if count >= sub_percent:
            break
    print(f"Coppied over {sub_percent} images to {subset_folder}")