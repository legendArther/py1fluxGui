import replicate
import os
import requests
from tkinter import Tk, Label, Button, Entry, OptionMenu, StringVar, IntVar, Checkbutton
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Initialize the Replicate client
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Function to generate and display images
def generate_image():
    prompt = prompt_entry.get()
    aspect_ratio = aspect_ratio_var.get()
    num_outputs = num_outputs_var.get()
    output_quality = output_quality_var.get()

    if not prompt:
        messagebox.showerror("Input Error", "Please enter a prompt.")
        return

    try:
        # Define the input for the model
        input_data = {
            "prompt": prompt,
            "seed": 0,  # Default seed
            "aspect_ratio": aspect_ratio,
            "output_format": "png",
            "num_outputs": num_outputs,
            "output_quality": output_quality,
        }

        # Run the model
        output = client.run(
            "black-forest-labs/flux-schnell", 
            input=input_data
        )

        # Handle the output (images)
        for index, item_url in enumerate(output):
            response = requests.get(item_url)
            response.raise_for_status()  # Check if the download was successful

            # Convert response to image
            image = Image.open(BytesIO(response.content))
            
            max_width, max_height = 500, 500
            image.thumbnail((max_width, max_height), Image.ANTIALIAS)

            # Save the image in the selected format
            image_filename = f"output_{index}.png"
            image.save(image_filename, format='png'.upper())

            # Display the image in the GUI
            img = ImageTk.PhotoImage(image)
            result_label.config(image=img)
            result_label.image = img 
           # messagebox.showinfo("Success", f"Image saved as {image_filename}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = Tk()
root.title("Flux Image Generator")
root.geometry("600x600")

# Label for the prompt entry field
prompt_label = Label(root, text="Enter your prompt:")
prompt_label.pack(pady=10)

# Entry widget to enter the prompt
prompt_entry = Entry(root, width=40)
prompt_entry.pack(pady=5)

# Aspect ratio selection
aspect_ratio_var = StringVar(root)
aspect_ratio_var.set("1:1")  # default value
aspect_ratio_label = Label(root, text="Select aspect ratio:")
aspect_ratio_label.pack(pady=10)
aspect_ratio_menu = OptionMenu(root, aspect_ratio_var, "1:1", "16:9")
aspect_ratio_menu.pack(pady=5)

# Number of outputs selection
num_outputs_var = IntVar(root)
num_outputs_var.set(1)  # default value
num_outputs_label = Label(root, text="Select number of outputs:")
num_outputs_label.pack(pady=10)
num_outputs_menu = OptionMenu(root, num_outputs_var, 1, 2, 3, 4)
num_outputs_menu.pack(pady=5)

# Output quality selection (0 to 100)
output_quality_var = IntVar(root)
output_quality_var.set(80)  # default value
output_quality_label = Label(root, text="Select output quality (0-100):")
output_quality_label.pack(pady=10)
output_quality_menu = OptionMenu(root, output_quality_var, *range(0, 101, 10))
output_quality_menu.pack(pady=5)

# Button to trigger the image generation
generate_button = Button(root, text="Generate Image", command=generate_image)
generate_button.pack(pady=20)

# Label to display the generated image
result_label = Label(root)
result_label.pack(pady=10)

# Run the GUI application
root.mainloop()
