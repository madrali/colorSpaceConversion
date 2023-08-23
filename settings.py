import os
import logging
import configparser

class Settings:
    def __init__(self, config_path="settings.cfg"):
        # Default values
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.image_path = ""
        self.filters = ['color']  # Default filter is 'color'
        self.save_temp = True  # Default is save temporary images
        self.temp_folder = "/tempImages"
        self.filtered_folder = "/filteredImages"  # Folder for filtered images
        self.filter_values = {
            'increaseContrast': 1.5,
            'decreaseContrast': 0.5
        }
        self.log_path = "/logs"
        self.setup_folders()

        if os.path.exists(self.config_path):
            self.load_settings()
        else:
            self.save_settings()

    def setup_folders(self):
        # Create necessary folders if they do not exist
        try:
            os.makedirs(self.temp_folder, exist_ok=True)
            os.makedirs(self.filtered_folder, exist_ok=True)  # Create folder for filtered images
            os.makedirs(self.log_path, exist_ok=True)
        except Exception as e:
            logging.error(f"An error occurred while creating directories: {e}")

    def load_settings(self):
        try:
            self.config.read(self.config_path)
            self.image_path = self.config.get('Settings', 'image_path')
            self.filters = self.config.get('Settings', 'filters').split(',')
            self.save_temp = self.config.getboolean('Settings', 'save_temp')
            self.filter_values['increaseContrast'] = self.config.getfloat('Settings', 'increaseContrast')
            self.filter_values['decreaseContrast'] = self.config.getfloat('Settings', 'decreaseContrast')
            self.log_path = self.config.get('Settings', 'log_path')

        except Exception as e:
            logging.error(f"An error occurred while loading settings from the .cfg file: {e}")

    def save_settings(self):
        try:
            self.config.add_section('Settings')
            self.config.set('Settings', 'image_path', self.image_path)
            self.config.set('Settings', 'filters', ','.join(self.filters))
            self.config.set('Settings', 'save_temp', str(self.save_temp))
            self.config.set('Settings', 'increaseContrast', str(self.filter_values['increaseContrast']))
            self.config.set('Settings', 'decreaseContrast', str(self.filter_values['decreaseContrast']))
            self.config.set('Settings', 'log_path', self.log_path)


            with open(self.config_path, 'w') as config_file:
                self.config.write(config_file)
        except Exception as e:
            logging.error(f"An error occurred while saving settings to the .cfg file: {e}")
