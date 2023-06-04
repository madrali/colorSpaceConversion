import cv2
import os
import logging
from itertools import permutations, product

# Create a logger
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

image_path = 'C:\\Users\\yigit\\Desktop\\111.jpg'
save_path = os.path.join(os.path.dirname(image_path), 'converted_images_plus_greenish\\')

gray_conversions = {
    'GRAY2BGR': cv2.COLOR_GRAY2BGR,
    'GRAY2RGB': cv2.COLOR_GRAY2RGB,
}

# Ensure that the directory exists
os.makedirs(save_path, exist_ok=True)

def ownConv(image):
    red_channel =image[:, :, 0]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 2]
    return cv2.merge([blue_channel, green_channel, red_channel])

def ownConv1(image):
    red_channel =image[:, :, 0]
    green_channel = image[:, :, 2]
    blue_channel = image[:, :, 1]
    return cv2.merge([blue_channel, green_channel, red_channel])

def ownConv2(image):
    red_channel =image[:, :, 1]
    green_channel = image[:, :, 0]
    blue_channel = image[:, :, 2]
    return cv2.merge([blue_channel, green_channel, red_channel])

def ownConv3(image):
    red_channel =image[:, :, 1]
    green_channel = image[:, :, 2]
    blue_channel = image[:, :, 0]
    return cv2.merge([blue_channel, green_channel, red_channel])

def ownConv4(image):
    red_channel =image[:, :, 2]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 0]
    return cv2.merge([blue_channel, green_channel, red_channel])

def ownConv5(image):
    red_channel =image[:, :, 2]
    green_channel = image[:, :, 0]
    blue_channel = image[:, :, 1]
    return cv2.merge([blue_channel, green_channel, red_channel])

conversions = {
    'BGR2RGB': cv2.COLOR_BGR2RGB,
    'RGB2BGR': cv2.COLOR_RGB2BGR,
    'BGR2HLS': cv2.COLOR_BGR2HLS,
    'HLS2BGR': cv2.COLOR_HLS2BGR,
    'RGB2HLS': cv2.COLOR_RGB2HLS,
    'HLS2RGB': cv2.COLOR_HLS2RGB,
    'BGR2GRAY': cv2.COLOR_BGR2GRAY,
    'RGB2GRAY': cv2.COLOR_RGB2GRAY,
    'ownConv': ownConv,
    'ownConv1': ownConv1,
    'ownConv2': ownConv2,
    'ownConv3': ownConv3,
    'ownConv4': ownConv4,
    'ownConv5': ownConv5,
 }
'''
this function is for all combinations 
saves all combinations of images in a folder
but it takes too much time
and i only need greenish images

def apply_filters(image_path):
    img = cv2.imread(image_path)

    for i in range(1,6):  #
        combo_save_path = os.path.join(save_path, f'{i}_combinations\\')
        os.makedirs(combo_save_path, exist_ok=True)

        for sequence in product(conversions.keys(), repeat=i):
            temp_img = img.copy()
            file_name = ""
            try:
                for conversion in sequence:
                    # if img become gray, stop.
                    if conversion.endswith("GRAY"):
                        temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                        file_name += conversion
                        break
                    elif conversion.startswith("ownConv"):
                        temp_img = conversions[conversion](temp_img)
                    else:
                        temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                    file_name += conversion + "_"
                cv2.imwrite(combo_save_path + file_name + '.jpg', temp_img)
            except cv2.error as e:
                print(f"Skipping {file_name} due to error: {e}")
                logger.error(f"Skipping {file_name} due to error: {e}")

apply_filters(image_path)
'''
def is_green_dominant(image):
    b, g, r = cv2.split(image)
    avg_b, avg_g, avg_r = b.mean(), g.mean(), r.mean()
    threshold = 10
    return avg_g - max(avg_b, avg_r) > threshold

def is_green_dominant(image):
    # Check if the image is colored
    if len(image.shape) == 3:
        b, g, r = cv2.split(image)
        avg_b, avg_g, avg_r = b.mean(), g.mean(), r.mean()

        # Set the threshold as you need
        threshold = 2
        return avg_g - max(avg_b, avg_r) > threshold
    else:
        # If the image is grayscale, it's not green-dominant
        return False

def apply_filters(image_path):
    img = cv2.imread(image_path)

    for i in range(1,6):  # I've changed this from 5 to 6 to include ownConv5
        combo_save_path = os.path.join(save_path, f'{i}_combinations\\')
        os.makedirs(combo_save_path, exist_ok=True)

        for sequence in product(conversions.keys(), repeat=i):
            temp_img = img.copy()
            file_name = ""
            try:
                for conversion in sequence:
                    # if img become gray, stop.
                    if conversion.endswith("GRAY"):
                        temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                        file_name += conversion
                        break
                    elif conversion.startswith("ownConv"):
                        temp_img = conversions[conversion](temp_img)
                    else:
                        temp_img = cv2.cvtColor(temp_img, conversions[conversion])
                    file_name += conversion + "_"

                # Check if the image is colored and if it is green-dominant
                if is_green_dominant(temp_img):
                    cv2.imwrite(combo_save_path + file_name + '.jpg', temp_img)
            except cv2.error as e:
                print(f"Skipping {file_name} due to error: {e}")
                logger.error(f"Skipping {file_name} due to error: {e}")

apply_filters(image_path)

