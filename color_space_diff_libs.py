import cv2
import os
import logging
from itertools import permutations
from PIL import Image
import numpy as np
import imageio
from skimage import io

# Create a logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

image_path = 'C:\\Users\\yigit\\Desktop\\111.jpg'
save_path = os.path.join(os.path.dirname(image_path), 'converted_images_DL\\')

# function dictionary
conversions = {
    'BGR2RGB': cv2.COLOR_BGR2RGB,
    'RGB2BGR': cv2.COLOR_RGB2BGR,
    'BGR2HLS': cv2.COLOR_BGR2HLS,
    'HLS2BGR': cv2.COLOR_HLS2BGR,
    'RGB2HLS': cv2.COLOR_RGB2HLS,
    'HLS2RGB': cv2.COLOR_HLS2RGB,
    'BGR2GRAY': cv2.COLOR_BGR2GRAY,
    'RGB2GRAY': cv2.COLOR_RGB2GRAY,
}

# after convert to gray, u cant do much

gray_conversions = {
    'GRAY2BGR': cv2.COLOR_GRAY2BGR,
    'GRAY2RGB': cv2.COLOR_GRAY2RGB,
}
os.makedirs(save_path, exist_ok=True)

def apply_filters(img, library_name):
    #  i only want to do up to 4 conversion
    for i in range(1,5):
        # creates new directory for each
        combo_save_path = os.path.join(save_path, library_name, f'{i}_combinations\\')
        os.makedirs(combo_save_path, exist_ok=True)

        for sequence in permutations(conversions.keys(), i):
            temp_img = img.copy()
            file_name = ""
            try:
                for conversion in sequence:
                    # if img become gray, stop.
                    if conversion.endswith("GRAY"):
                        temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                        file_name += conversion
                        break
                    temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                    file_name += conversion + "_"
                cv2.imwrite(combo_save_path + file_name + '.jpg', temp_img)
            except cv2.error as e:
                print(f"Skipping {file_name} due to error: {e}")
                logger.error(f"Skipping {file_name} due to error: {e}")

def apply_filters_pillow(image_path):
    # trying to open a file with Pillow and convert it to RGB
    img = Image.open(image_path).convert('RGB')
    img = np.array(img)
    # then trying to same thing. is there any diffrence?
    apply_filters(img, 'pillow')

def apply_filters_imageio(image_path):
    # trying to open a file with imgio and convert it to RGB
    img = imageio.imread(image_path)
    # any diffrence ?
    apply_filters(img, 'imageio')

def apply_filters_skimage(image_path):
    # trying to open a file image_path and convert it to RGB
    img = io.imread(image_path)
    # Convert the image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # is there any diffrence ?
    apply_filters(img, 'skimage')

def apply_filters_opencv(image_path):
    # Read an image file with OpenCV
    img = cv2.imread(image_path)
    # Call the original apply_filters function
    apply_filters(img, 'opencv')

# Call the functions
apply_filters_pillow(image_path)
apply_filters_imageio(image_path)
apply_filters_skimage(image_path)
apply_filters_opencv(image_path)
