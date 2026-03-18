# 🖼️ URL Image Viewer - Streamlit App

A beautiful, user-friendly web application to automatically display product images from Excel URLs. Perfect for reviewing product catalogs, validating image links, or creating automated slideshows.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

- 🎨 **Beautiful UI** - Clean, modern interface with gradient styling
- 🔄 **Auto-advance Mode** - Automatic slideshow with countdown timer
- ⚙️ **Flexible Controls** - Manual navigation (First, Previous, Next, Last)
- 📊 **Product Information** - Display name, price, category, SKU, and more
- 🎯 **Smart Filtering** - Remove empty URLs automatically
- 📈 **Progress Tracking** - Visual progress bar and viewing history
- 💾 **Download Images** - Save current image with one click
- 🔍 **Jump to Row** - Quick navigation to specific products
- 📱 **Responsive Design** - Works on desktop and mobile

## 🚀 Quick Start

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/url-image-viewer.git
cd url-image-viewer
```

2. **Install dependencies**
```bash
pip install -r requirements_streamlit.txt
```

3. **Run the app**
```bash
streamlit run streamlit_app.py
```

4. **Open your browser**
The app will automatically open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud (FREE!)

### Option 1: Deploy via Streamlit Cloud Dashboard

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://streamlit.io/cloud)**

3. **Sign in with GitHub**

4. **Click "New app"**

5. **Fill in the details:**
   - Repository: `yourusername/url-image-viewer`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

6. **Click "Deploy"** 🚀

Your app will be live at: `https://yourusername-url-image-viewer.streamlit.app`

### Option 2: Deploy via Command Line

1. **Install Streamlit CLI**
```bash
pip install streamlit
```

2. **Login to Streamlit Cloud**
```bash
streamlit login
```

3. **Deploy**
```bash
streamlit deploy streamlit_app.py
```

## 📖 How to Use

### 1. Upload Your Excel File
- Click "Upload Excel File" in the sidebar
- Supported formats: `.xlsx`, `.xls`, `.csv`

### 2. Configure Settings
- **URL Column**: Select which column contains your image URLs
- **Display Time**: Set how long each image shows (3-60 seconds)
- **Auto-advance**: Enable automatic slideshow mode
- **Range Selection**: Choose which rows to view

### 3. Navigate Images
- **Manual Mode**: Use Previous/Next buttons
- **Auto Mode**: Click Play to start slideshow
- **Jump**: Go directly to any row number

### 4. View Product Details
- See product name, price, category, SKU
- Open URL in new tab
- Download current image

## 📋 Excel File Format

Your Excel file should have at least one column with image URLs:

| url_1                              | product_name | price  | category    |
|------------------------------------|--------------|--------|-------------|
| https://example.com/image1.jpg     | Product A    | $19.99 | Electronics |
| https://example.com/image2.png     | Product B    | $29.99 | Clothing    |
| https://example.com/image3.jpg     | Product C    | $39.99 | Home        |

**Recognized Columns** (auto-detected):
- **Product Name**: `product_name`, `Product Name`, `name`, `title`
- **Description**: `description`, `Description`, `desc`
- **Price**: `price`, `Price`, `cost`
- **Category**: `category`, `Category`, `department`
- **SKU/Barcode**: `sku`, `SKU`, `barcode`, `product_id`

## 🎨 Screenshots

### Main Interface
Beautiful, clean interface with product image and details side-by-side.

### Auto-advance Mode
Automatic slideshow with countdown timer.

### Product Information
Comprehensive product details display.

## 🛠️ Configuration

### Environment Variables (Optional)

Create a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
```

## 🔧 Customization

### Change Display Time Range
Edit `streamlit_app.py`:
```python
display_seconds = st.slider(
    "Display Time (seconds)",
    min_value=3,      # Change minimum
    max_value=60,     # Change maximum
    value=15,         # Change default
    step=1
)
```

### Modify Color Scheme
Edit the CSS in `streamlit_app.py`:
```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
    }
</style>
""", unsafe_allow_html=True)
```

## 📦 Dependencies

- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `openpyxl` - Excel file handling
- `Pillow` - Image processing
- `requests` - HTTP requests for images

See `requirements_streamlit.txt` for specific versions.

## 🐛 Troubleshooting

### Images Not Loading
- ✅ Check if URLs are valid (start with `http://` or `https://`)
- ✅ Verify URLs point to actual images
- ✅ Some sites block automated requests - try different sources
- ✅ Check internet connection

### Upload Size Limit
Streamlit Cloud has a 200MB upload limit by default. For larger files:
1. Split your Excel file into smaller chunks
2. Or deploy locally with no limits

### Slow Loading
- Increase timeout in the code (default: 10 seconds)
- Check image server response time
- Try reducing image quality/size at source

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💡 Tips

1. **Test First**: Upload a small file (5-10 rows) to test before processing large datasets
2. **Auto-advance**: Great for hands-free product reviews
3. **History**: Check sidebar to see which items you've already viewed
4. **Download**: Save images for offline reference
5. **Jump Feature**: Quickly navigate to flagged items

## 🌟 Use Cases

- 📦 **Product Catalog Review** - Validate product images
- 🛒 **E-commerce QA** - Check image quality and links
- 📊 **Data Validation** - Verify URLs are working
- 🎨 **Content Review** - Quick visual inspection
- 📸 **Image Collection** - Download multiple images easily

## 📞 Support

If you encounter issues:
1. Check the [Issues](https://github.com/yourusername/url-image-viewer/issues) page
2. Create a new issue with details
3. Or contact: your.email@example.com

## 🎉 Acknowledgments

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Pillow](https://python-pillow.org/)

---

**Made with ❤️ for easy product image viewing**

⭐ Star this repo if you find it useful!
