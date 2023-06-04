# Color Space Conversion Effects on Ai Traning

## Description
This repository contains Python scripts that apply various color space conversions to images using different image reading libraries. The purpose of these scripts is to investigate the effects of different image reading libraries and commonly used color space conversions on output images. The results can be used to understand how these variations might influence the training of various AI models. 

## Features
- Reads images using four different libraries: OpenCV, Pillow, imageio, and scikit-image.
- Applies various color space conversions to the images (using only OpenCV for now).
- Saves the converted images in separate directories for each library and each combination of conversions.
- Logs any errors that occur during the conversion process.

## Potential Usage

### Computer Vision 
Color space conversions can highlight or hide certain features of an image, which can be beneficial for image analysis or processing.

### Data Augmentation
Applying various transformations to images can expand the dataset used to train a machine learning model, improving its ability to generalize and preventing overfitting.

### Image Comparison
By comparing the results of different image reading and conversion libraries, you can determine which library is most suitable for a particular task.
