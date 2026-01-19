import streamlit as st
from docx import Document
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Text to Image Encoder",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #FF6B6B;
        font-size: 2.5rem;
    }
    .stSubheader {
        color: #4ECDC4;
    }
    </style>
""", unsafe_allow_html=True)

# Function to extract text from a DOCX file
def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return None

# Function to extract text from TXT file
def extract_text_from_txt(file):
    """Extract text from TXT file"""
    try:
        text = file.read().decode("utf-8")
        return text
    except Exception as e:
        st.error(f"Error reading TXT file: {e}")
        return None

# Function to convert text to binary
def text_to_binary(text):
    """Convert text to binary representation"""
    if not text:
        return ""
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

# Function to convert binary string to image with custom colors
def binary_to_image(binary_string, bit_size=2, color_1=(255, 165, 0), color_0=(0, 0, 139)):
    """Convert binary string to pixelated image"""
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

# Function to convert image back to binary
def image_to_binary(img, color_1_rgb, color_0_rgb):
    """Convert image back to binary string"""
    pixels = img.load()
    width, height = img.size
    binary_string = ""
    
    # Define tolerance for color matching
    tolerance = 30
    
    for y in range(0, height, 2):  # Assuming bit_size=2
        for x in range(0, width, 2):
            pixel = pixels[x, y]
            
            # Check which color it's closer to
            dist_to_1 = sum((pixel[i] - color_1_rgb[i])**2 for i in range(3)) ** 0.5
            dist_to_0 = sum((pixel[i] - color_0_rgb[i])**2 for i in range(3)) ** 0.5
            
            binary_string += '1' if dist_to_1 < dist_to_0 else '0'
    
    return binary_string

# Function to convert binary back to text
def binary_to_text(binary_string):
    """Convert binary string back to text"""
    text = ""
    for i in range(0, len(binary_string) - 7, 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

# Streamlit UI
st.title("🖼️ Text to Image Encoder")

st.markdown("""
    ### Transform Your Words Into Art
    Save your precious words as unique pixelated images. Upload a document and watch it transform into visual data!
""")

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 Upload & Convert")
    
    # Tab selection
    tab1, tab2 = st.tabs(["Text to Image", "Image to Text"])
    
    with tab1:
        # File uploader
        uploaded_file = st.file_uploader("Choose a file", type=["docx", "txt"])
        
        if uploaded_file is not None:
            # Extract text based on file type
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_docx(uploaded_file)
            else:
                text = extract_text_from_txt(uploaded_file)
            
            if text:
                st.success(f"✅ Extracted {len(text)} characters")
                
                # Display extracted text (limited)
                with st.expander("👀 View Extracted Text"):
                    st.text_area("Extracted Text:", value=text[:500] + "..." if len(text) > 500 else text, height=150, disabled=True)
    
    with tab2:
        st.write("Upload an encoded image to decode it back to text")
        image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        if image_file is not None:
            st.info("Image decoding feature - Configure colors first to decode")

with col2:
    st.subheader("🎨 Customize Colors")
    
    # Color pickers in sidebar for better UX
    col_a, col_b = st.columns(2)
    
    with col_a:
        color_1 = st.color_picker("Color for '1' bits", "#FFA500", key="color1")  # Orange
    
    with col_b:
        color_0 = st.color_picker("Color for '0' bits", "#00008B", key="color2")  # Dark Blue
    
    st.subheader("⚙️ Image Settings")
    
    bit_size = st.slider("Pixel Size (bit_size)", min_value=1, max_value=10, value=2, 
                        help="Size of each bit in pixels. Larger = bigger image")

# Main conversion area
if uploaded_file is not None and text:
    st.divider()
    st.subheader("🔄 Conversion Process")
    
    # Create three columns for stats
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    # Convert text to binary
    binary_equivalent = text_to_binary(text)
    
    with stat_col1:
        st.metric("Characters", len(text))
    
    with stat_col2:
        st.metric("Binary Bits", len(binary_equivalent))
    
    with stat_col3:
        image_dimension = int((len(binary_equivalent) ** 0.5))
        st.metric("Image Size", f"{image_dimension}×{image_dimension}")
    
    # Convert hex color to RGB tuple
    color_1_rgb = tuple(int(color_1[i:i+2], 16) for i in (1, 3, 5))
    color_0_rgb = tuple(int(color_0[i:i+2], 16) for i in (1, 3, 5))

    # Convert binary to image with custom colors
    with st.spinner("🎨 Generating image..."):
        image = binary_to_image(binary_equivalent, bit_size=bit_size, color_1=color_1_rgb, color_0=color_0_rgb)
    
    st.divider()
    st.subheader("✨ Generated Image")
    
    # Display the image
    col_image1, col_image2 = st.columns([2, 1])
    
    with col_image1:
        st.image(image, caption="Your Pixelated Data Art", use_column_width=True)
    
    with col_image2:
        st.info("""
        **Image Details:**
        - Format: PNG
        - Each pixel represents a bit
        - Orange = 1, Blue = 0
        - 100% lossless encoding
        """)
    
    st.divider()
    st.subheader("💾 Download & Share")
    
    # Save image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    col_download1, col_download2 = st.columns(2)
    
    with col_download1:
        st.download_button(
            label="📥 Download as PNG",
            data=img_bytes,
            file_name=f"encoded_{Path(uploaded_file.name).stem}.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col_download2:
        # Save binary to text file
        binary_bytes = io.BytesIO(binary_equivalent.encode())
        st.download_button(
            label="📄 Download Binary Code",
            data=binary_bytes,
            file_name=f"binary_{Path(uploaded_file.name).stem}.txt",
            mime="text/plain",
            use_container_width=True
        )

# Footer
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.markdown("### 👤 Creator")
    st.write("**Ishank Mishra**")

with col_footer2:
    st.markdown("### 📧 Contact")
    st.write("[Email Me](mailto:your-email@example.com)")

with col_footer3:
    st.markdown("### 🤝 Collaborate")
    st.write("Open for group projects and collaboration!")