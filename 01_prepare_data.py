# 1. Download data and place it in the data folder
# 2. Make id table from images.txt
# 3. Split out the files between training and test based on "train_test_split.txt"
# 4. Augment the data using img_aug.py
import json
import os
from dataclasses import dataclass
from pathlib import Path
from PIL import Image
import six.moves
import tarfile
import requests
import zipfile
import pydicom as dicom
import cv2
from sklearn.model_selection import train_test_split

from img_aug import create_data_augumentation

if __name__ == '__main__':

    zip_file_name = "rsna-pneumonia-detection-challenge.zip"
    zip_folder = "datasets/rsna-pneumonia-detection-challenge"

    jpeg_folder = "datasets/rsna-pneumonia-detection-challenge-jpeg"
    jpeg_path = Path(jpeg_folder)
    if not jpeg_path.exists():
        jpeg_path.mkdir()

    train_folder = f"{jpeg_folder}/train"
    train_path = Path(train_folder)
    if not train_path.exists():
        train_path.mkdir()

    test_folder = f"{jpeg_folder}/test"
    test_path = Path(test_folder)
    if not test_path.exists():
        test_path.mkdir()

    test_detected_folder = f"{jpeg_folder}/test/detected"
    test_detected_path = Path(test_detected_folder)
    if not test_detected_path.exists():
        test_detected_path.mkdir()

    train_detected_folder = f"{jpeg_folder}/train/detected"
    train_detected_path = Path(train_detected_folder)
    if not train_detected_path.exists():
        train_detected_path.mkdir()

    test_free_folder = f"{jpeg_folder}/test/free"
    test_free_path = Path(test_free_folder)
    if not test_free_path.exists():
        test_free_path.mkdir()

    train_free_folder = f"{jpeg_folder}/train/free"
    train_free_path = Path(train_free_folder)
    if not train_free_path.exists():
        train_free_path.mkdir()

    train_folder = f"{jpeg_folder}/train"
    zip_file_name = f"{zip_folder}.zip"
    pneumonia_exits = {}  # key is patient_id, value = binary detection. 1=detected, 0=not detected

    datasets_path = Path("datasets")
    destination = Path(f'{zip_file_name}')
    if not datasets_path.exists():
        datasets_path.mkdir()
        # TODO - download the zip

    datasets_pneumonia_detection_out_path = Path(zip_folder)
    if not datasets_pneumonia_detection_out_path.exists():
        datasets_pneumonia_detection_out_path.mkdir()

    if destination.exists():  # TODO, skip this step for now
        if ".tgz" in zip_file_name:
            tar = tarfile.open(destination, 'r:gz')
            tar.extractall("datasets")
            tar.close()
        elif ".zip" in zip_file_name:
            # Check to see if files already exist
            count = 0
            for f in Path(zip_folder).glob("**/*"):
                if f.is_file():
                    count += 1

            if count == 0:
                print(f"Unzipping {destination}")
                with zipfile.ZipFile(destination, 'r') as zip_ref:
                    zip_ref.extractall(str(datasets_pneumonia_detection_out_path))
            else:
                print(f"File count: {count}. Not unzipping")

    # Read all the pneumonia target data
    csv_file = open("datasets/rsna-pneumonia-detection-challenge/stage_2_train_labels.csv")
    x_data = []
    y_data = []
    for line in csv_file:
        split_line = line.split(",")
        if len(split_line) == 6:
            patient_id = split_line[0]
            if "patientId" in patient_id:
                continue
            detected = split_line[5]
            # print(f"{patient_id} detected: {detected}")
            x_data.append(patient_id)
            y_data.append(detected.strip())
            pneumonia_exits[patient_id] = detected.strip()
    # print(x_data)
    # print(y_data)
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.33, random_state=4, stratify=y_data)
    print(f"x_train size: {len(x_train)} x_test size: {len(x_test)}")

    # Convert DCM images to jpeg

    # Check to see if files already exist
    count = 0
    for f in jpeg_path.glob("**/*"):
        if f.is_file():
            count += 1

    if count == 0:
        print("Time to convert dmc to jpeg")
        for f in Path(zip_folder).glob("stage_2_train_images/*.dcm"):

            file_split = str(f).split("/")
            print(file_split)
            # skip test
            if "test" in file_split[2]:
                continue

                # Take the image id and find if its part of the train or test set.
            # then figure out if Pneumonia is detected or not
            patient_id = file_split[-1].replace(".dcm", "")
            image_directory = ""
            if patient_id in x_train:
                index = x_train.index(patient_id)
                if y_train[index] == "1":
                    image_directory = train_detected_folder
                else:
                    image_directory = train_free_folder
            else:
                index = x_test.index(patient_id)
                if y_test[index] == "1":
                    image_directory = test_detected_folder
                else:
                    image_directory = test_free_folder

            # Now copy image into correct directory
            print(f)
            print(f"patient_id:{patient_id} detected: ", end=" ")
            ds = dicom.dcmread(str(f))
            pixel_array_numpy = ds.pixel_array
            file_name = f"{image_directory}/{patient_id}.jpg"
            print("Creating", file_name)
            cv2.imwrite(file_name, pixel_array_numpy)

    create_data_augumentation(jpeg_folder, "train")
    print("Finished processing the data")
