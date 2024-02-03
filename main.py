import os
import cv2
import shutil
import numpy as np
from datetime import datetime, timedelta
import json
import random
import threading
import time
import platform
import pyautogui

def simple_resize_image(img, target_width=800, max_height=480):
        img_resized = cv2.resize(img, (target_width, max_height))
        return img_resized

class PiPhotoStand:
    #FULLSCREEN = False
    
    WINDOW_HEIGHT = 480
    WINDOW_WIDTH = 800
    IMAGE_DISPLAY_TIME = 5  # seconds
    IMAGE_CALENDER_CYCLE_TIME = 5  # seconds
    EXIT_PIXEL_RANGE = 100
    pyautogui.PAUSE = 1

    def __init__(self, server_folder):
        self.exit_program = False
        self.day_change = False
        self.server_folder = server_folder
        images_folder = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/MY_IMAGES"
        self.images_folder = images_folder
        self.init_folders()

        self.history_data = {}
        self.past_images = []
        self.current_image = None
        self.get_current_timestamp()
        self.load_history_data()
        
        self.time_thread = threading.Thread(target=self.time_interrupt, daemon=True)
        self.mouse_thread = threading.Thread(target=self.mouse_clb, daemon=True)
        self.mouse_thread.start()
        
        if self.is_raspberry_pi_zero_2():
            print("Running on PI. Entering fullscreen mode.")
            self.FULLSCREEN = True
        else:
            self.FULLSCREEN = False

        self.display_images_calender()

    def time_interrupt(self):

        while not self.exit_program:
            # get seconds
            self.get_current_timestamp()
            self.load_history_data()
            current_time = datetime.now().second
            print(f"Current time: {current_time}")
            if current_time >= 55:
                self.past_images.append(self.current_image)
                self.current_image = None
                self.day_change = True

            # if self.last_year != self.current_year or self.last_month != self.current_month or self.last_date != self.current_date:
#               self.past_images.append(self.current_image)
                #self.current_image = None
                #self.day_change = True
            #     print("Day change detected!")
                
            time.sleep(5)

    def mouse_clb(self):
        while not self.exit_program:
            x, y = pyautogui.position()
            if x < self.EXIT_PIXEL_RANGE and y < self.EXIT_PIXEL_RANGE:
                print("Exiting the program.")
                self.exit_program = True
            time.sleep(5)

    def init_folders(self):
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)

        self.list_files(self.server_folder)
        self.list_files(self.images_folder)
        self.copy_images(source_folder=server_folder, destination_folder=self.images_folder)

    def set_mouse_to_bottom_right(self):
        if self.is_raspberry_pi_zero_2():
            # Get the screen resolution
            screen_width, screen_height = pyautogui.size()

            # Set the mouse cursor to the bottom right corner
            pyautogui.moveTo(screen_width - 1, screen_height - 1)

    def copy_images(self, source_folder:str, destination_folder:str):
        if not os.path.exists(source_folder):
            print("The 'images' folder does not exist.")
            return

        image_extensions = ['.png', '.jpg', '.jpeg', '.gif']

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        for filename in os.listdir(source_folder):
            if any(filename.lower().endswith(ext) for ext in image_extensions):
                source_path = os.path.join(source_folder, filename)
                destination_path = os.path.join(destination_folder, filename)

                if not os.path.exists(destination_path):
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: {filename}")
                else:
                    print(f"Skipped (already exists): {filename}")

    def list_files(self, folder_path):
        if not os.path.exists(folder_path):
            print("The folder does not exist.")
            return None

        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        print(f"Files in {folder_path}: ", files)
        return files

    def is_raspberry_pi_zero_2(self):
        try:
            # Check if the platform is 'armv6l' and if the model is 'Zero2W'
            return platform.machine() == 'armv6l' and platform.system() == 'Linux' and 'Zero2W' in platform.uname().release
        except Exception:
            return False
    
    def get_current_timestamp(self):
        self.current_date = datetime.now().day
        self.current_month_year = datetime.now().strftime("%B %Y")
        self.current_month = datetime.now().strftime("%B")
        self.current_year = datetime.now().strftime("%Y")
        _current_month_days = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        self.days_in_month = _current_month_days.day
        #self.days_in_month = 31

    def write_history_data(self):
        self.history_data["past_images"] = self.past_images
        self.history_data["today"] = {}
        self.history_data["today"]["year"] = self.current_year
        self.history_data["today"]["month"] = self.current_month
        self.history_data["today"]["date"] = self.current_date
        self.history_data["today"]["current_image"] = self.current_image   
        # write history data as json to the images folder
        with open(f"{self.images_folder}/history_data.json", "w") as f:
            json.dump(self.history_data, f)

    def load_history_data(self):
        # load history data from the images folder
        try:
            with open(f"{self.images_folder}/history_data.json", "r") as f:
                self.history_data = json.load(f)
                self.past_images = self.history_data["past_images"]
                self.current_image = self.history_data["today"]["current_image"]
                self.last_year = self.history_data["today"]["year"]
                self.last_month = self.history_data["today"]["month"]
                self.last_date = self.history_data["today"]["date"]
                print(f"History data loaded!")

        except FileNotFoundError:
            print("History data file not found.")
            self.history_data = {}
            self.past_images = []
            self.current_image = None
        except json.JSONDecodeError:
            print("History data file is empty.")
            self.history_data = {}
            self.past_images = []
            self.current_image = None

    def clear_history_data(self):
        self.history_data = {}
        self.past_images = []
        self.current_image = None
        self.write_history_data()

    def overlay_calendar(self,img):
        
        self.get_current_timestamp()
        # Create a black background for the calendar overlay
        overlay = np.zeros_like(img)

        # Define the font and text properties
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_thickness = 1
        font_color = (255, 255, 255)  # White color
        font_scale_month = 1
        font_thickness_month = 2
        # Display the month and dates on the overlay
        cv2.putText(overlay, self.current_month_year, (22, img.shape[0] - 85),
                    font, font_scale_month, font_color, font_thickness_month, cv2.LINE_AA)

        # Calculate the position to start displaying dates
        date_x, date_y = 20, img.shape[0] - 50
        max_dates_per_row = 16  # Maximum number of dates per row

        max_date_width, max_date_height = cv2.getTextSize("31", font, font_scale, font_thickness)[0]

        date_spacing = int((self.WINDOW_WIDTH - 40 - max_date_width) / 36)

        # Display dates for the current month

        dates_in_row = 0
        for day in range(1, self.days_in_month + 1):
            date_text = str(day)
            date_width, date_height = cv2.getTextSize(date_text, font, font_scale, font_thickness)[0]
            # Check if the maximum number of dates per row is reached
            if dates_in_row == max_dates_per_row:
                date_x = 20  # Reset x position for the new row
                date_y += date_height + 15  # Adjust y position for the new row
                dates_in_row = 0

            cv2.putText(overlay, date_text, (date_x, date_y),
                        font, font_scale, font_color, font_thickness, cv2.LINE_AA)

            # Mark the current date with a white circle
            if day == self.current_date:
                center = (date_x + date_width // 2, date_y - date_height // 2)
                radius = 14
                cv2.circle(overlay, center, radius, (255, 255, 255), 2)  # White circle for the current date

            date_x += max_date_width + date_spacing
            dates_in_row += 1

        # Blend the overlay with the original image
        alpha = 0.6
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

        return img

    def resize_image_for_display(self, img, size=(WINDOW_WIDTH,WINDOW_HEIGHT)):
        screen_ratio = size[1] / size[0]
        # height/width
        img_ratio = img.shape[0] / img.shape[1]

        #print(f"Screen ratio: {screen_ratio}, Image ratio: {img_ratio}")

        if screen_ratio > img_ratio:
            # Screen is taller than the image
            new_width = size[0]
            new_height = int(new_width * img_ratio)
            # Create a background image
            img_resized = cv2.resize(img, (size[0], size[1]))
            img_resized = cv2.GaussianBlur(img_resized, (21, 21), 0)
            y_offset = (size[1] - new_height) // 2
            img_resized[y_offset:y_offset + new_height, 0:new_width] = cv2.resize(img, (new_width, new_height))
        else:
            # Screen is wider than the image
            new_height = size[1]
            new_width = int(new_height / img_ratio)
            # Create a background image
            img_resized = cv2.resize(img, (size[0], size[1]))
            img_resized = cv2.GaussianBlur(img_resized, (15, 15), 0)
            x_offset = (size[0] - new_width) // 2
            img_resized[0:new_height, x_offset:x_offset + new_width] = cv2.resize(img, (new_width, new_height))

        return img_resized

    def display_images_random(self):
        # Pick a random file from the images folder
        image_files = [filename for filename in os.listdir(self.images_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        available_images = [img for img in image_files if img not in self.past_images]
        while not self.exit_program:
            while available_images is not None and len(available_images) > 0 and not self.exit_program:
                selected_image = random.choice(available_images)
                
                self.current_image = selected_image
                image_path = os.path.join(self.images_folder, selected_image)
                img = cv2.imread(image_path)
                img = self.resize_image_for_display(img)
                img = self.overlay_calendar(img)
                if self.FULLSCREEN:
                    #cv2.namedWindow('my_window', cv2.WINDOW_FULLSCREEN)
                    cv2.namedWindow("my_window", cv2.WND_PROP_FULLSCREEN)          
                    cv2.setWindowProperty("my_window", cv2.WND_PROP_FULLSCREEN, 1)
                else:
                    #cv2.namedWindow('my_window', cv2.WINDOW_NORMAL)
                    cv2.namedWindow('my_window')
                cv2.imshow("my_window", img)
                cv2.waitKey(self.IMAGE_DISPLAY_TIME*1000)
                self.past_images.append(selected_image)
                available_images = [img for img in image_files if img not in self.past_images]
                self.write_history_data()

            print("No more available images.")
            self.clear_history_data()
        cv2.destroyAllWindows()
        self.mouse_thread.join()

    def adjust_brightness(self, image, factor):
        """
        Adjust the brightness of an image.

        Parameters:
        - image: Input image (OpenCV format)
        - factor: Brightness adjustment factor (1.0 for no change, values less than 1.0 for darkening, values greater than 1.0 for brightening)

        Returns:
        - Brightness-adjusted image
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        v = hsv[:, :, 2]
        v = np.clip(factor * v, 0, 255)
        hsv[:, :, 2] = v
        adjusted_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return adjusted_image

    def display_images_calender(self):
        self.time_thread.start()
        selected_image = None
        # Pick a random file from the images folder
        image_files = [filename for filename in os.listdir(self.images_folder) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        available_images = [img for img in image_files if img not in self.past_images]

        while not self.exit_program:
            if len(available_images) == 0:
                print("No images available. Refreshing list!")
                self.clear_history_data()
                available_images = [img for img in image_files if img not in self.past_images]
                self.current_image = None

            while self.day_change is False and not self.exit_program:
                if self.current_image is None:
                    selected_image = random.choice(available_images)
                    self.current_image = selected_image
                    print("Selected new image: ", selected_image)
                else:
                    selected_image = self.current_image

                self.write_history_data()
                image_path = os.path.join(self.images_folder, selected_image)
                img = cv2.imread(image_path)
                img = self.resize_image_for_display(img)
                img = self.adjust_brightness(img, 1.2)
                img = self.overlay_calendar(img)
                
                if self.FULLSCREEN:
                    cv2.namedWindow("my_window", cv2.WND_PROP_FULLSCREEN)          
                    cv2.setWindowProperty("my_window", cv2.WND_PROP_FULLSCREEN, 1)
                else:
                    cv2.namedWindow('my_window', cv2.WINDOW_NORMAL)
                cv2.imshow("my_window", img)
                cv2.waitKey(self.IMAGE_CALENDER_CYCLE_TIME*1000)
                self.set_mouse_to_bottom_right()
                
            available_images = [img for img in image_files if img not in self.past_images]
            self.write_history_data()
            self.day_change = False

        cv2.destroyAllWindows()
        self.time_thread.join()
        self.mouse_thread.join()

if __name__ == "__main__":
    current_user = os.getenv('USER')
    server_folder = f'/home/{current_user}/TE_NAS_photo_share'
    my_photo_stand = PiPhotoStand(server_folder=server_folder)
    my_photo_stand.time_thread.join()

