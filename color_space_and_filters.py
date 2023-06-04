import cv2
import os
import logging
import coloredlogs
from itertools import permutations, product
from PIL import Image, ImageFilter
import numpy as np

logger = logging.getLogger()
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
coloredlogs.install(level='DEBUG', logger=logger)

image_path = 'C:\\Users\\yigit\\Desktop\\111.jpg'
save_path = os.path.join(os.path.dirname(image_path), 'converted_images\\')

# Function dictionary
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

# After convert to gray, u cant do much
gray_conversions = {
    'GRAY2BGR': cv2.COLOR_GRAY2BGR,
    'GRAY2RGB': cv2.COLOR_GRAY2RGB,
}

# added difrent filters
filters = [ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.DETAIL, ImageFilter.EDGE_ENHANCE,
           ImageFilter.EDGE_ENHANCE_MORE,
           ImageFilter.EMBOSS, ImageFilter.FIND_EDGES, ImageFilter.SHARPEN, ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE]

filter_names = ['blur', 'contour', 'detail', 'edge_enhance', 'edge_enhance_more', 'emboss', 'find_edges', 'sharpen',
                'smooth', 'smooth_more']


os.makedirs(save_path, exist_ok=True)


def apply_filters(image_path):
    # cv2.imread assume file is bgr, right ?
    img = cv2.imread(image_path)

    # Apply each possible conversions
    for i in range(1, 5):
        # Create a new directory for each combination
        combo_save_path = os.path.join(save_path, f'{i}_combinations\\')
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
                # log the current conversion process
                logger.info(f'Applying conversion: {file_name}')

                # apply filters
                for j in range(min(5, len(filters))):
                    temp_img_filter = temp_img.copy()
                    # Apply filter
                    temp_img_pil = Image.fromarray(temp_img_filter)
                    temp_img_filter = temp_img_pil.filter(filters[j])
                    temp_img_filter = np.array(temp_img_filter)

                    # Save result
                    cv2.imwrite(os.path.join(combo_save_path, file_name + '_' + filter_names[j] + '.jpg'),
                                temp_img_filter)
                    # Log the current filter process
                    logger.info(f'Applying filter: {filter_names[j]} on {file_name}')

            except cv2.error as e:
                print(f"Skipping {file_name} due to error: {e}")
                logger.error(f"Skipping {file_name} due to error: {e}")


apply_filters(image_path)
