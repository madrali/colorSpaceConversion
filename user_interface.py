import tkinter

import PIL


class UserInterface:
    def __init__(self, window, image_capture):
        self.window = window
        self.image_capture = image_capture

        self.panelA = None
        self.panelB = None


    # burada ImageCapture'dan aldığınız `update_panel` kodunu yerleştirin

    def update_panel(self, original_image, filtered_image):
        """
        This method updates the display panel with the given images.
        """

        # Convert the images to PIL and ImageTK format
        original_image = PIL.Image.fromarray(original_image)
        filtered_image = PIL.Image.fromarray(filtered_image)

        # Resize images
        original_image = original_image.resize((600, 600), PIL.Image.ANTIALIAS)
        filtered_image = filtered_image.resize((600, 600), PIL.Image.ANTIALIAS)

        # Display images
        original_image = PIL.ImageTk.PhotoImage(original_image)
        filtered_image = PIL.ImageTk.PhotoImage(filtered_image)

        # Initialize or update panels
        if self.panelA is None or self.panelB is None:
            self.panelA = tkinter.Label(image=original_image)
            self.panelA.image = original_image
            self.panelA.grid(row=0, column=1, sticky="nsew")

            self.panelB = tkinter.Label(image=filtered_image)
            self.panelB.image = filtered_image
            self.panelB.grid(row=0, column=2, sticky="nsew")
        else:
            self.panelA.configure(image=original_image)
            self.panelB.configure(image=filtered_image)
            self.panelA.image = original_image
            self.panelB.image = filtered_image

    def ui(self):
        # burada 'App' sınıfınızdan `ui` metodundaki kodu yerleştirin.
        def ui(self):
            # Create Menu bar
            self.menubar = tkinter.Menu(self.window)

            # Add commands to the Menu bar
            self.commands_menu = tkinter.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="File", menu=self.commands_menu)

            self.filters_Menu = tkinter.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="Filters", menu=self.filters_Menu)

            """
            creating command menu buttons
            """
            self.commands_menu.add_command(label="Select New Image", command=self.select_image, accelerator="F1")
            self.commands_menu.add_command(label="Save Image", command=self.snapshot, accelerator="F2")
            self.commands_menu.add_command(label="Select Area", command=self.select_area, accelerator="1")
            self.filters_Menu.add_command(label="Remove Filters", command=self.no_filter, accelerator="2")
            self.filters_Menu.add_command(label="Contrast Increase", command=self.increaseContrast_filter,
                                          accelerator="3")
            self.filters_Menu.add_command(label="Contrast Decrease", command=self.decreaseContrast_filter,
                                          accelerator="4")
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

            self.window.config(menu=self.menubar)

            self.canvas = tkinter.Canvas(self.window, width=1250, height=650)
            self.canvas.grid(row=0, column=0, rowspan=10, columnspan=5)

            # self.window.tk.call('wm', 'iconphoto', self.window._w, tkinter.PhotoImage(file='test-images/icon.png'))
        # However, you'll need to replace all instances of `self.img_cap` with `self.image_capture`,
        # and `self.window` will already be defined.
        pass
