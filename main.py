#Project for comp photo

import PySimpleGUI as sg
from PIL import Image
import io

# Function to convert PIL Image to bytes for PySimpleGUI
def convert_to_bytes(image, max_size=(800, 600)):
    image.thumbnail(max_size)
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        data = output.getvalue()
    return data

# Define the layout of the GUI
layout = [
    [sg.Button("Open Image", key="-OPEN-"), sg.Button("Exit")],
    [sg.Image(key="-IMAGE-")]
]

# Create the window
window = sg.Window("Image Viewer", layout, resizable=True)

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
                img = Image.open(file_path)
                img_bytes = convert_to_bytes(img)
                
                # Update the image element with the new image
                window["-IMAGE-"].update(data=img_bytes)
                
            except Exception as e:
                sg.popup_error("Failed to open image:", e)

# Close the window
window.close()