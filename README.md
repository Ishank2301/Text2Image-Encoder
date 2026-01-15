# Doc2Pixel: Binary Visualization of Textual Data

Doc2Pixel is a Streamlit-based application that converts textual data from DOCX files into a visual pixel representation by encoding characters into binary form. Each bit is mapped to a colored pixel, transforming documents into unique, reproducible images.

This project explores alternative data representations by bridging text processing, binary encoding, and visual computing.

---

## 🚀 Features

- Upload and process `.docx` files
- Convert text into binary (8-bit ASCII encoding)
- Visualize binary data as pixel-based images
- Custom color selection for binary `0` and `1`
- Automatic square image generation with padding
- Download generated images
- Clean and interactive Streamlit UI

---

## 🧠 Conceptual Overview

The transformation pipeline is:
DOCX File → Plain Text → Binary Encoding → Pixel Mapping → Image Output

### Encoding Logic
- Each character is converted into its 8-bit binary representation
- Binary digits are arranged sequentially into a near-square grid
- Each bit is rendered as a colored pixel block:
  - `1` → User-defined color
  - `0` → User-defined color

The resulting image is a deterministic visual fingerprint of the document content.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – UI & app framework
- **python-docx** – DOCX text extraction
- **Pillow (PIL)** – Image creation and pixel manipulation

---

## 📂 Project Structure
  ├── app.py
  ├── requirements.txt
  ├── assets/
  │ ├── example_image.png
  │ └── preview.png
  └── README.md

  
---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/Doc2Pixel.git
cd Doc2Pixel
2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
streamlit run app.py

📸 Example Output

A document such as the Bhagavad Gita or any text-heavy DOCX file can be transformed into a single image representing its binary structure.

Different texts generate visually distinct patterns.

💡 Use Cases

Creative data visualization

Educational tool for understanding binary encoding

Artistic representation of textual data

Document fingerprinting concepts

Exploratory work in digital representation and encoding

🔮 Future Enhancements

Reverse decoding (Image → Binary → Text)

Encryption layer before binary conversion

Support for additional file formats (PDF, TXT)

Multiple encoding schemes (UTF-8, Base64, Hex)

Pattern-based pixel layouts (spiral, zig-zag)

Adjustable pixel scaling

Metadata embedding inside images

👤 Author

Ishank Mishra
B.Tech | Machine Learning & Software Development
Open to collaboration and research-based projects

📄 License

This project is licensed under the MIT License.
