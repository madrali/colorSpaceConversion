import settings
import image_capture
import user_interface
import cv2
import logging
from image_capture import ImageCapture


class ImageManipulator:
    def __init__(self, img_cap, logger):
        self.img_cap = img_cap
        self.logger = logger
        self.isImageInstantiated = False

    def select_image(self, event=None):
        self.img_cap = ImageCapture()
        self.img_cap.update('color')
        self.isImageInstantiated = True


    def select_area(self):
        self.img_cap.clear_rois()
        self.window.iconify()

        try:
            """
             Image Resize and store pixel ratios for applying filters to original size
            """
            resized_image = cv2.resize(self.img_cap.original_image, (600, 600))
            original_shape = self.img_cap.original_image.shape
            resized_shape = resized_image.shape

            x_ratio = original_shape[1] / resized_shape[1]
            y_ratio = original_shape[0] / resized_shape[0]

            # List to store the coordinates of the ROIs

            while True:
                # Create a copy of the resized_image to display the ROI selection
                self.temp_image = resized_image.copy()

                # Let the user select a ROI
                rect = cv2.selectROI("Select a ROI (Press ENTER when done, press c to continue to the next)",
                                     self.temp_image,
                                     False)
                rect_temp = rect

                logging.info(f"ROI Coordinates selected: {rect_temp} x ratio= {x_ratio} y ratio ={y_ratio}")

                # If the rect size is 0, this means the user pressed ESC, so we break the loop
                if rect[2] == 0 and rect[3] == 0:
                    break

                # Convert the ROI coordinates back to the original image scale and store before convert
                rect = (
                    int(rect[0] * x_ratio), int(rect[1] * y_ratio), int(rect[2] * x_ratio), int(rect[3] * y_ratio))
                logging.info(f"ROI Coordinates: {rect}")

                # Add the ROI coordinates to the list
                self.img_cap.add_roi(rect)
                # Draw the selected ROI on the resized_image we use rect temp bcs we still see resized
                x, y, w, h = rect_temp
                cv2.rectangle(resized_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Log the ROI coordinates

            # Close all OpenCV windows
            cv2.destroyAllWindows()
            # Close all OpenCV windows
            self.img_cap.update_panel(self.temp_image, self.img_cap.original_image)
            cv2.destroyAllWindows()

            self.window.deiconify()
        except Exception as e:
            self.logger.error(f"An error occurred when selecting a ROI: {e}")

    def no_filter(self):
        try:
            self.logger.info("All filters removed.")
        except Exception as e:
            self.logger.error(f"An error occurred when clearing filters: {e}")

    def increaseContrast_filter(self):
        try:
            if self.isImageInstantiated:
                self.img_cap.update('increaseContrast')
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'increaseContrast' filter: {e}")

    # Other functions here...
    def no_filter(self):
        """
        Clear all filters.
        """

        try:
            # this will be use when multiple filters avalible
            # self.settings.filters.clear()
            self.logger.info("All filters removed.")
        except Exception as e:
            self.logger.error(f"An error occurred when clearing filters: {e}")

    def increaseContrast_filter(self):
        try:
            if self.isImageInstantiated:
                # this will be use when multiple filters avalible
                # self.img_cap.all_filters = SELECT_FILTER('increaseContrast', True)
                self.img_cap.update('increaseContrast')
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'increaseContrast' filter: {e}")

    def decreaseContrast_filter(self):
        """
        Apply the 'decreaseContrast' filter.
        """

        try:
            if self.isImageInstantiated:
                # this will be use when multiple filters avalible
                # self.img_cap.all_filters = SELECT_FILTER('decreaseContrast', True)
                self.img_cap.update('decreaseContrast')


        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'decreaseContrast' filter: {e}")

    def gray_filter(self):
        """
        Apply the 'gray' filter.
        """

        try:
            if self.isImageInstantiated:
                # this will be use when multiple filters avalible
                # self.img_cap.all_filters = SELECT_FILTER('gray', True)
                self.img_cap.update('gray')
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'gray' filter: {e}")

    def bgr_filter(self):
        """
        Apply the 'gray' filter.
        """

        try:
            if self.isImageInstantiated:
                # this will be use when multiple filters avalible
                # self.img_cap.all_filters = SELECT_FILTER('gray', True)
                self.img_cap.update('bgr')
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'gray' filter: {e}")



    def hls_filter(self):
        """
        Apply the 'gray' filter.
        """

        try:
            if self.isImageInstantiated:
                # this will be use when multiple filters avalible
                # self.img_cap.all_filters = SELECT_FILTER('gray', True)
                self.img_cap.update('hls')
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'hls' filter: {e}")

