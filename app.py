import streamlit as st
from docx import Document
from PIL import Image

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

# Function to convert text to binary
def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

# Function to convert binary string to image with custom colors for 1 and 0
def binary_to_image(binary_string, bit_size=2, color_1=(255, 165, 0), color_0=(0, 0, 139)):
    num_bits = len(binary_string)
    pixels_per_row = int((num_bits ** 0.5))
    if pixels_per_row * pixels_per_row < num_bits:
        pixels_per_row += 1

    padded_binary = binary_string.ljust(pixels_per_row ** 2, '0')
    
    image_size = pixels_per_row * bit_size
    img = Image.new('RGB', (image_size, image_size), "white")
    pixels = img.load()

    for i, bit in enumerate(padded_binary):
        row = (i // pixels_per_row) * bit_size
        col = (i % pixels_per_row) * bit_size
        color = color_1 if bit == '1' else color_0

        for x in range(bit_size):
            for y in range(bit_size):
                pixels[col + x, row + y] = color

    return img

# Streamlit UI
st.title("Word to Image Converter")

# Add some text
st.write("Save words close to your heart as images. Just upload the doc file and generate an image representing whole doc as pixels.")

# Load an image (ensure the image file is in the same directory or provide the correct path)
image = Image.open("BhagavadGita.png")

# Display the image
st.image(image, caption="This is an example image of Whole Bhagavad Gita wrapped into a single image.", use_container_width=True)
# Upload file
uploaded_file = st.file_uploader("Choose a DOCX file", type="docx")

# Color pickers for 1 and 0 bits
color_1 = st.color_picker("Pick a color", "#FFA500")  # Default Orange
color_0 = st.color_picker("Pick another one", "#00008B")  # Default Dark Blue

if uploaded_file is not None:
    # Extract text from the uploaded DOCX file
    text = extract_text_from_docx(uploaded_file)
    
    # Convert text to binary
    binary_equivalent = text_to_binary(text)
    
    # Convert hex color to RGB tuple
    color_1_rgb = tuple(int(color_1[i:i+2], 16) for i in (1, 3, 5))
    color_0_rgb = tuple(int(color_0[i:i+2], 16) for i in (1, 3, 5))

    # Convert binary to image with custom colors
    image = binary_to_image(binary_equivalent, color_1=color_1_rgb, color_0=color_0_rgb)
    
    # Display the image
    st.image(image, caption="Generated Pixelated Image", use_column_width=True)
    
    # Save image to a temporary file and provide download link
    image.save("binary_image.png")
    
    with open("binary_image.png", "rb") as file:
        st.download_button("Download Image", file, file_name="binary_image.png", mime="image/png")
st.write("Created by- Ishank Mishra")
st.write("Contact me for group projects and collaboration.")
youtube_logo = Image.open("BhagavadGita.png")
