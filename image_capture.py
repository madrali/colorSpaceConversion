import logging
import os
import random
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import PIL.Image
import PIL.ImageFilter
import PIL.ImageTk
import cv2
import numpy as np

from settings import Settings


class ImageCapture :
    """
    This class represents an image capture which has filters applied to it.
    """
    counter = 1

    def __init__(self, window=None, settings=None):
        self.original_image = None
        self.rois_to_filter = []
        self.logger = logging.getLogger(__name__)
        self.window = window
        self.settings = settings if settings is not None else Settings()

        # Select the image using a new dialog window.
        self.img_path = tkinter.filedialog.askopenfilename()

        # If a path was selected, load and display the image.
        if len(self.img_path) > 0:
            try:
                # self.original_imageFinal = cv2.cvtColor(cv2.imread(self.img_path), cv2.COLOR_BGR2RGB)
                # self.original_image = cv2.cvtColor(cv2.imread(self.img_path), cv2.COLOR_BGR2RGB)

                #
                #
                # self.original_imageFinal = cv2.imread(self.img_path)

                self.logger.info(f"Loaded image from {self.img_path}")
                self.filtered_image = None
                self.panelA = None
                self.panelB = None
                # self.update_panel(self.original_image, self.original_image)
            except Exception as e:
                error_message = f"An error occurred: {e} try again with different photo"
                self.logger.error(error_message)
                tkinter.messagebox.showerror("Error", error_message)

    # def getRealDeal(self):
    #     return self.original_imageFinal
    def update_panel(self, original_image, filtered_image):
        """
        This method updates the display panel with the given images.
        """
        # print(type(original_image))  # Check the type of original_image
        # print(original_image.shape)  # Check the shape of original_image
        # print(original_image.dtype)  # Check the data type of original_image

        # # Convert the images to PIL and ImageTK format
        # original_image = PIL.Image.fromarray(original_image)
        #
        # original_imageFULLsizePIL = original_image.copy()
        #
        # filtered_image = PIL.Image.fromarray(filtered_image)
        #
        # # Resize images
        # original_image = original_image.resize((600, 600), PIL.Image.ANTIALIAS)
        # filtered_image = filtered_image.resize((600, 600), PIL.Image.ANTIALIAS)
        #
        # # Display images
        # original_imageDisplay = PIL.ImageTk.PhotoImage(original_image)
        # filtered_imageDisplay = PIL.ImageTk.PhotoImage(filtered_image)

        # Initialize or update panels
        if self.panelA is None or self.panelB is None:
            self.panelA = tkinter.Label(image=original_imageDisplay)
            self.panelA.image = original_image
            self.panelA.grid(row=0, column=1, sticky="nsew")

            self.panelB = tkinter.Label(image=filtered_imageDisplay)
            self.panelB.image = filtered_image
            self.panelB.grid(row=0, column=2, sticky="nsew")
        else:
            self.panelA.configure(image=original_imageDisplay)
            self.panelB.configure(image=filtered_imageDisplay)
            self.panelA.image = original_imageDisplay
            self.panelB.image = filtered_imageDisplay

    def add_roi(self, roi):
        """
        This method adds a region of interest to the list of regions to filter.
        """
        self.rois_to_filter.append(roi)

    def clear_rois(self):
        """
        This method clears the list of regions of interest to filter.
        """
        self.rois_to_filter.clear()


    def update(self, filter, folderPath):
        """
        This method updates the filtered image based on the regions of interest and filters selected.
        """

        # Ensure original image exists
        if hasattr(self, 'original_image'):

            # Initialize filtered image as a copy of the original
            self.filtered_image = self.original_imageFinal.copy()
            # Log the initial ROIs

            # Apply the selected filters to each ROI region
            for roi in self.rois_to_filter:

                rois_str = ', '.join(str(roi) for roi in self.rois_to_filter)
                self.logger.info(f"Initial ROIs: {rois_str}")
                x, y, w, h = roi
                roi_image = self.original_imageFinal[y:y + h, x:x + w]

                # for multiple filters
                #
                # for filter_name in main.filter_dic:
                #     roi_image = self.apply_filter(filter_name, roi_image)
                self.logger.info(f"{filter} filter applied to ROI")

                # just 1 filter

                roi_image = self.apply_filter(filter, roi_image,folderPath)
                self.logger.info(f"{filter} filter applied to ROI: {roi}")

                # Replace the ROI in the filtered image with the filtered ROI
                # self.original_imageFinal[y:y + h, x:x + w] = roi_image
                # cv2.imwrite(os.path.join(folderPath, f"Original image final_{self.counter}.png"), self.original_imageFinal)
                # self.original_image = PIL.Image.fromarray(self.original_imageFinal)
                # self.original_image = self.original_image.resize((600, 600), PIL.Image.ANTIALIAS)
                #
                # self.original_image= self.filtered_image

                # Save the intermediate filtered ROI if required

            # Save the final filtered image
            cv2.imwrite(os.path.join(folderPath, "filtered_image.png"), self.original_imageFinal)

            # Update the display
            self.update_panel(self.original_image, self.filtered_image)

        else:
            self.logger.error("FILTER COULDNT APPLIED ")

    def apply_filter(self, filter_name, roi_image,folder ):

        # logging.warning(f"filter name{filter_name}, {roi_image}")

        if filter_name == 'color':
            pass
        elif filter_name == 'gray':
            roi_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2GRAY)
            roi_image = cv2.cvtColor(roi_image, cv2.COLOR_GRAY2RGB)
        elif filter_name == 'increaseContrast':
            alpha = random.uniform(1.0, 2.0)
            beta = random.uniform(0, 80)
            roi_image = cv2.addWeighted(roi_image, alpha, np.zeros(roi_image.shape, roi_image.dtype), 0, beta)
        elif filter_name == 'decreaseContrast':
            alpha = random.uniform(1.0, 0.8)
            beta = random.uniform(-100, 0)
            roi_image = cv2.addWeighted(roi_image, alpha, np.zeros(roi_image.shape, roi_image.dtype), 0, beta)

        elif filter_name == 'hls':

             roi_image = cv2.cvtColor(roi_image, cv2.COLOR_RGB2HLS)
             # roi_image = cv2.cvtColor(roi_image, cv2.COLOR_HLS2RGB)

        elif filter_name == 'bgr':
            roi_image = cv2.cvtColor(roi_image, cv2.COLOR_BGR2RGB)
            red_channel = roi_image[:, :, 0]
            green_channel = roi_image[:, :, 1]
            blue_channel = roi_image[:, :, 2]
            roi_image = cv2.merge([blue_channel, green_channel, red_channel])
            roi_image = cv2.cvtColor(roi_image, cv2.COLOR_RGB2BGR)

        try:
            if self.settings.save_temp:
                cv2.imwrite(os.path.join(folder, f"roiImage_{self.counter}.png"), roi_image)
                self.counter += 1
        except Exception as e:
            self.logger.error(f"An error occurred when saving the temp ROI img : {e}")

        return roi_image
