import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog

import pandas as pd
from numpy.core.defchararray import isdigit

from PicsData import Picture, load_data_pics
from main import choose_pic, extract_data, show_image


# this function will run the app and will be called from the main.py file
def run_App():
    def load_data():
        # run the preprocessEdfToCsv.exe file as a subprocess
        subprocess.run("preprocessEdfToCsv.exe")

    def show_single_participant():
        # run the ExtractDataEDFv_2.exe file as a subprocess - this will create the Data.csv file
        # subprocess.run("ExtractDataEDFv_2.exe")
        # time.sleep(5)
        # Ask the user for the path of the images dataset
        data_path = simpledialog.askstring("Input", "Enter the path of the images dataset:",
                                           parent=root)
        images = load_data_pics(data_path)
        # Ask the user for the image index
        index = simpledialog.askinteger("Input", "Enter the index of the image to display:",
                                        parent=root, minvalue=0, maxvalue=100000000)

        if index is not None:
            # Add code to display a picture for the selected participant index and dataset path
            # ...
            print(f"Displaying image for participant {index} from path {data_path}")
        else:
            print("No index entered.")
        df = pd.read_csv('Data.csv', header=0, delimiter=",")


        # Create a new window
        eye_movement_window = tk.Toplevel(root)
        eye_movement_window.title("Eye Movement Visualization")
        image_name, width, height, image_id, image_category_id = choose_pic(images, index)
        chosen_image = Picture(image_name, width, height, image_id, image_category_id)
        image_idx = chosen_image.image_id
        # in df search for the image index and from the line of the index bring me the trail number
        # Search for the image index in the DataFrame
        matching_row = df[df['image_index num'] == image_idx]
        trail_number = matching_row.loc[:, 'trail number'].values[0].T

        # Check if a matching row is found
        if matching_row.empty:
            print(f"No trail number found for image index {image_idx}")

        x, y = show_image(matching_row, image_name, width, height, trail_number, 1, eye_movement_window)
        # add to Data.csv the headers from the df
        df.to_csv('Data.csv', header=True, index=False)
        # Make sure to call the mainloop() on the new window to keep it active
        eye_movement_window.mainloop()

    def show_multi_participant():
        # Ask the user for the path of the images dataset
        data_path = simpledialog.askstring("Input", "Enter the path of the images dataset:",
                                           parent=root)
        if data_path is not None:
            # Ask the user for the image index
            index = simpledialog.askinteger("Input", "Enter the index of the image to display:",
                                            parent=root, minvalue=0, maxvalue=100000000)

            if index is not None:
                # Add code to display a picture for the selected participant index and dataset path
                # ...
                print(f"Displaying image for participant {index} from path {data_path}")
            else:
                print("No index entered.")
        else:
            print("No path entered.")
        images = load_data_pics(data_path)
        image_name, width, height, image_id, image_category_id = choose_pic(images, index)
        chosen_image = Picture(image_name, width, height, image_id, image_category_id)
        image_idx = chosen_image.image_id
        df = extract_data(image_idx)
        # Create a new window
        eye_movement_window = tk.Toplevel(root)
        eye_movement_window.title("Eye Movement Visualization")
        found = False
        for image in images:
            if image.image_id == image_idx[0]:
                found = True
                image_name, width, height, image_id, image_category_id = image.image_name, image.image_size, image.image_size, image.image_id, image.image_category_id
                chosen_image = Picture(image_name, width, height, image_id, image_category_id)
                trail_numbers = df.loc[:, 'trail number'].values.T
                x_axis_padding, y_axis_padding = show_image(df, image_name, width, height, trail_numbers, 2, eye_movement_window)
        if not found:
            print("Image not found. Please make sure to enter a valid image ID or image name.")

            # Call the function to extract data for the specified image index
            extracted_data = extract_data(image_idx)

            # Display the extracted data
            print(extracted_data)
            eye_movement_window.mainloop()

    # Create the main application window
    root = tk.Tk()
    root.title("EyeMovement Visualizer")

    # Set the window size
    root.geometry("600x300")  # Width x Height

    # Create a welcome label
    welcome_label = tk.Label(root, text="Welcome to the EyeMovement Visualizer", font=("Helvetica", 16, "bold"))
    welcome_label.pack(pady=20)

    # Create buttons with some styling
    button_style = {"font": ("Helvetica", 12), "padx": 20, "pady": 10, "bg": "#A7585F", "fg": "white"}

    load_button = tk.Button(root, text="Load Data", command=load_data, **button_style)
    single_button = tk.Button(root, text="Single Participant", command=show_single_participant, **button_style)
    multi_button = tk.Button(root, text="Multi Participant", command=show_multi_participant, **button_style)

    # Pack buttons
    load_button.pack()
    single_button.pack()
    multi_button.pack()

    # Start the GUI event loop
    root.mainloop()


run_App()
