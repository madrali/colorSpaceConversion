import sys
import tkinter.filedialog
import time
import os
import cv2
from tkinter import Menu, Tk, filedialog
from tkinter import messagebox
import logging
from warnings import filters

from PIL import ImageTk,Image

from image_capture import ImageCapture
import settings

# first making sure about our files then starting logger

folderImg = "/filteredImages"
folderLog = "/logs"
folderTemp = "/temp"
folderTemp2day = "/temp-" + time.strftime("%d-%m-%Y_%H-%M")

# if important paths doesnt exist then crate
# path error is a flag for beign sure we succesfully create paths.

cwd = os.getcwd()

path = cwd + folderImg
if not os.path.exists(path):
    try:
        os.makedirs(path)
    except Exception as e:
        sys.exit("permission denied"+e)

pathLog = cwd + folderLog
if not os.path.exists(pathLog):
    try:
        os.makedirs(pathLog)
    except Exception as e:
        sys.exit("permission denied" + e)

folderTemp = cwd + folderTemp
if not os.path.exists(folderTemp):
    try:
        os.makedirs(folderTemp)
    except Exception as e:
        sys.exit("permission denied" + e)

folderTemp2day = folderTemp + folderTemp2day
if not os.path.exists(folderTemp2day):
    try:
        os.makedirs(folderTemp2day)
    except Exception as e:
        sys.exit("permission denied" + e)


# logger configs
logFileName = pathLog + '/FilterY_' + time.strftime("%d-%m-%Y_%H-%M-%S") + ".log"
logging.basicConfig(filename=logFileName, level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

# this func will be use but not now

# def SELECT_FILTER(filter, status):
#     # change required filter to true
#     filter_dic = {x: False for x in fil}  # change all values to false in dictionary to make only filter to true
#     if filter in filter_dic:
#         assert type(status) == bool
#         filter_dic[filter] = status
#     return filter_dic
#   avalible filter list
#
#   fil = ['color', 'gray', 'threshold', 'increaseContrast', 'decreaseContrast', ]
#   filter_dic = {}
#        these will be added
#        'logTransformation', 'powerLowEnhancement','histogramEqualization
#        'negativeEnhancement', 'gauss', 'sobel', 'laplace', 'min', 'max', 'median', 'average', 'unsharp', 'prewitt',
#

class App:
    """
    Main application class.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, window, window_title):

        self.window = window
        self.window.title(window_title)

        # Initialize the settings and image capture
        self.settings = settings.Settings()
        self.img_cap = ImageCapture
        self.isImageInstantiated = False


        # Create ui
        self.ui()

        # After	it is called once, the update method will be automatically called every loop
        self.delay = 30
        self.window.mainloop()

    def ui(self):

        # Create Menu bar
        self.menubar = Menu(self.window)

        # Add commands to the Menu bar
        self.commands_menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.commands_menu)

        self.filters_Menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Filters", menu=self.filters_Menu)

        """
        creating command menu buttons
        """
        self.commands_menu.add_command(label="Select New Image", command=self.select_image, accelerator="F1")
        self.commands_menu.add_command(label="Save Image", command=self.snapshot, accelerator="F2")
        self.commands_menu.add_command(label="Select Area", command=self.select_area, accelerator="1")
        self.filters_Menu.add_command(label="Remove Filters", command=self.no_filter, accelerator="2")
        self.filters_Menu.add_command(label="Contrast Increase", command=self.increaseContrast_filter, accelerator="3")
        self.filters_Menu.add_command(label="Contrast Decrease", command=self.decreaseContrast_filter, accelerator="4")
        self.filters_Menu.add_command(label="Gray", command=self.gray_filter, accelerator="g")
        self.filters_Menu.add_command(label="HLS", command=self.hls_filter, accelerator="h")
        self.filters_Menu.add_command(label="BGR", command=self.bgr_filter, accelerator="b")



        ##################################################################################################

        self.window.bind("<F1>", lambda _: self.select_image())
        self.window.bind("<F2>", lambda _: self.snapshot())
        self.window.bind("1", lambda _: self.select_area())
        self.window.bind("2", lambda _: self.no_filter())
        self.window.bind("3", lambda _: self.increaseContrast_filter())
        self.window.bind("4", lambda _: self.decreaseContrast_filter())
        self.window.bind("g", lambda _: self.gray_filter())
        self.window.bind("h", lambda _: self.hls_filter())
        self.window.bind("b", lambda _: self.bgr_filter())

        bg_image = Image.open(os.path.join(os.getcwd()+'/img', "bg-ins.png"))
        # Convert the Image object to a PhotoImage object (Tkinter compatible)
        bg_photoimage = ImageTk.PhotoImage(bg_image)


        self.window.config(menu=self.menubar)

        self.canvas = tkinter.Canvas(self.window, width=1200, height=628)
        self.canvas.grid(row=0, column=0, rowspan=10, columnspan=5)

        self.canvas.create_image(0, 0, image=bg_photoimage, anchor='nw')
        self.canvas.image = bg_photoimage  # keep a reference!

        # self.window.tk.call('wm', 'iconphoto', self.window._w, tkinter.PhotoImage(file='test-images/icon.png'))

    def select_image(self, event=None):
        # create instance from image capture
        self.img_cap = ImageCapture()
        # self.img_cap.all_filters = SELECT_FILTER('color', True)
        self.img_cap.update('color',folderTemp2day)
        self.isImageInstantiated = True

    def select_area(self):
        if hasattr(self.img_cap, 'original_image'):
            self.img_cap.clear_rois()
            self.window.iconify()

            try:
                """
                 Image Resize and store pixel ratios for applying filters to original size
                """
                resized_image = cv2.resize(self.img_cap.original_image, (600, 600))
                original_resized = cv2.resize(self.img_cap.original_image, (600, 600))
                original_resized = cv2.cvtColor(original_resized,cv2.COLOR_RGB2BGR)
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
                                         original_resized,
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
                    cv2.rectangle(original_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Log the ROI coordinates

                # Close all OpenCV windows
                cv2.destroyAllWindows()
                # Close all OpenCV windows
                self.img_cap.update_panel(self.temp_image, self.img_cap.original_image)
                cv2.destroyAllWindows()

                self.window.deiconify()
            except Exception as e:
                self.logger.error(f"An error occurred when selecting a ROI: {e}")
        else:
            self.logger.error("Without any img, i cant do anything.")

    def snapshot(self,img):
        """
        Save the current image.
        """

        try:
            # self.image_cap.update('color')
            self.logger.info("Snapshot taken.")
        except Exception as e:
            self.logger.error(f"An error occurred when taking a snapshot: {e}")

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
                self.img_cap.update('increaseContrast',folderTemp2day)
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
                self.img_cap.update('decreaseContrast',folderTemp2day)


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
                self.img_cap.update('gray',folderTemp2day)
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
                self.img_cap.update('bgr',folderTemp2day)
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
                self.img_cap.update('hls',folderTemp2day)
        except Exception as e:
            self.logger.error(f"An error occurred when applying the 'hls' filter: {e}")



app = App(tkinter.Tk(), 'ROI FilterMaster')
