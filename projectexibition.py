import tkinter as tk
from tkinter import filedialog
from PIL import Image

def encode(image_file, message):
    # Open the image file
    with Image.open(image_file) as image:
        # Get the image width and height
        width, height = image.size

        # Convert the message to binary
        message_binary = ''.join(format(ord(x), 'b').zfill(8) for x in message)

        # Add padding to the message if necessary
        message_binary += '0' * ((8 - len(message_binary) % 8) % 8)

        # Convert the message binary to a list of integers
        message_int = [int(message_binary[i:i+8], 2) for i in range(0, len(message_binary), 8)]

        # Convert the image to a list of pixels
        pixels = list(image.getdata())

        # Create a new list of pixels with the message
        new_pixels = [(r, g, b, m) for (r, g, b), m in zip(pixels, message_int)]

        # Create a new image with the new pixels
        new_image = Image.new(image.mode, image.size)
        new_image.putdata(new_pixels)

        # Return the new image
        return new_image

def decode(image_file):
    # Open the image file
    with Image.open(image_file) as image:
        # Convert the image to a list of pixels
        pixels = list(image.getdata())

        # Get the message from the pixels
        message_int = [t[3] for t in pixels]

        # Convert the message back to binary
        message_binary = ''.join(format(i, 'b').zfill(8) for i in message_int)

        # Remove the padding from the message
        message_binary = message_binary.rstrip('0')

        # Convert the message binary to a string
        message = ''.join(chr(int(message_binary[i:i+8], 2)) for i in range(0, len(message_binary), 8))

        # Return the message
        return message

class IMG_Stegno:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Steganography")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.image_file = tk.StringVar()
        self.image_label = tk.Label(self.root, text="No image selected")
        self.image_button = tk.Button(self.root, text="Select image", command=self.select_image)

        self.message_entry = tk.Entry(self.root)
        self.message_label = tk.Label(self.root, text="Enter message")

        self.encode_button = tk.Button(self.root, text="Encode", command=self.encode)
        self.decode_button = tk.Button(self.root, text="Decode", command=self.decode)

    def encode(self):
        # Get the message from the entry field
        message = self.message_entry.get()

        # Encode the message into the image
        image = encode(self.image_file.get(), message)

        # Open a file dialog to select a save location
        save_file = filedialog.asksaveasfilename()

        # Save the image
        image.save(save_file)

    def decode(self):
        # Get the message from the image
        message = decode(self.image_file.get())

        # Display the message
        tk.messagebox.showinfo("Decoded message", message)

    def main(self, root):
        self.image_label.pack()
        self.image_button.pack()
        self.message_label.pack()
        self.message_entry.pack()
        self.encode_button.pack()
        self.decode_button.pack()
        root.mainloop()

    def select_image(self):
        # Open a file dialog to select an image
        self.image_file.set(filedialog.askopenfilename())

        # Update the image label with the image file name
        self.image_label.config(text=self.image_file.get())