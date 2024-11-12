#Project for comp photo

import PySimpleGUI as sg
from PIL import Image
import io

# Function to convert PIL Image to bytes for PySimpleGUI
def convert_to_bytes(image, max_size=(500, 500)):
    # Resize the image to the max size while maintaining aspect ratio
    image.thumbnail(max_size)
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        data = output.getvalue()
    return data

def save_image_as_png(image):
    # Open a file save dialog to choose where to save the image
    save_path = sg.popup_get_file("Save image as", save_as=True, file_types=(("PNG Files", "*.png"),), no_window=True)
    
    if save_path:
        try:
            # Ensure the file has a .png extension
            if not save_path.lower().endswith('.png'):
                save_path += '.png'
            
            # Save the image as PNG
            image.save(save_path, format="PNG")
            sg.popup("Image saved successfully!", save_path)
        except Exception as e:
            sg.popup_error("Failed to save image:", e)

# Define the layout of the GUI
layout = [
    [
        sg.Column([
            [sg.Text("Original Image")],
            [sg.Image(key="-LEFT-")]
        ], element_justification="center"),
        
        sg.VerticalSeparator(),
        
        sg.Column([
            [sg.Text("Modified Image")],
            [sg.Image(key="-RIGHT-")]
        ], element_justification="center")
    ],
    [sg.Button("Open Image", key="-OPEN-"), sg.Button("Save Image", key="-SAVE-"), sg.Button("Exit")]
]

# Create the window
window = sg.Window("Image Viewer", layout, resizable=True, size=(1400, 700))

# Variable to store the opened image and the modified image
original_image = None
modified_image = None

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event == "-OPEN-":
        # Open a file dialog to select an image
        file_path = sg.popup_get_file(
            "Choose an image",
            file_types=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif"),),
            no_window=True
        )
        
        if file_path:
            try:
                # Open the image using PIL
                original_image = Image.open(file_path)
                modified_image = original_image.copy()  # Make a copy of the image for modifications
                
                # Convert both images to bytes for display
                original_img_bytes = convert_to_bytes(original_image)
                modified_img_bytes = convert_to_bytes(modified_image)
                
                # Update both image elements
                window["-LEFT-"].update(data=original_img_bytes)  # Display the original on the left
                window["-RIGHT-"].update(data=modified_img_bytes)  # Display the modified on the right
                
            except Exception as e:
                sg.popup_error("Failed to open image:", e)
    elif event == "-SAVE-":
        if modified_image:
            save_image_as_png(modified_image)
        else:
            sg.popup("No image loaded", "Please open an image first.")

# Close the window
window.close()