'''
 colorSpaceConversionPyScript
 Author: @madrali
 Description: In this script, we read an image and create different variations of it
 by applying various color space conversions using Python and the OpenCV library.

 Date: June 2, 2023 Signature: You, the person downloading this script and running it,
 should know what it does. You are responsible for what you do with this script and the
 results it produces. Don't blame me if something goes wrong.
 License: MIT License
'''

import cv2
import os
from itertools import permutations

image_path = 'C:\\Users\\yigit\\Desktop\\111.jpg'
save_path = os.path.join(os.path.dirname(image_path), 'converted_images\\')

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

# Ensure that the directory exists
os.makedirs(save_path, exist_ok=True)

def apply_filters(image_path):
    # cv2.imread assume file is bgr, right ?
    img = cv2.imread(image_path)

    # Apply each possible  conversions
    # for i in range(1, len(conversions) + 1):
    # apply max 4 filters

    for i in range(1,5):

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
                cv2.imwrite(save_path + file_name + '.jpg', temp_img)
            except cv2.error as e:
                print(f"Skipping {file_name} due to error: {e}")

apply_filters(image_path)