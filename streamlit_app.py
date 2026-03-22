"""
URL Image Viewer - Streamlit App
Automatically display images from Excel URLs with a beautiful UI
"""

import streamlit as st
import pandas as pd
import time
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Set page config
st.set_page_config(
    page_title="URL Image Viewer",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    .product-info {
        background: #e9ecef;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .countdown {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'auto_advance' not in st.session_state:
    st.session_state.auto_advance = False
if 'viewing_history' not in st.session_state:
    st.session_state.viewing_history = []

def create_session_with_retries():
    """Create requests session with retry logic"""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=0.3,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def load_image_from_url(url, timeout=10):
    """Load image from URL with error handling"""
    try:
        session = create_session_with_retries()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = session.get(url, timeout=timeout, headers=headers)
        response.raise_for_status()
        
        # Check if response is an image
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type.lower():
            return None, f"URL does not point to an image (Content-Type: {content_type})"
        
        img = Image.open(BytesIO(response.content))
        return img, None
    except requests.exceptions.Timeout:
        return None, "Timeout: Image took too long to load"
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_product_info(row, url_column):
    """Extract product information from row"""
    info = {}
    
    # Get product name
    name_columns = ['product_name', 'Product Name', 'name', 'Name', 'title', 'Title']
    for col in name_columns:
        if col in row.index and pd.notna(row[col]):
            info['name'] = str(row[col])
            break
    
    # Get description
    desc_columns = [
        'description', 'Description', 'DESCRIPTION',
        'desc', 'Desc', 'DESC',
        'product_description', 'Product Description', 'Product_Description', 
        'Full Description',
        'details', 'Details', 'DETAILS',
        'info', 'Info', 'INFO',
        'about', 'About', 'ABOUT'
    ]
    for col in desc_columns:
        if col in row.index and pd.notna(row[col]):
            info['description'] = str(row[col])
            break
    
    # Get price
    price_columns = ['price', 'Price', 'cost', 'Cost']
    for col in price_columns:
        if col in row.index and pd.notna(row[col]):
            info['price'] = str(row[col])
            break
    
    # Get category
    category_columns = ['category', 'Category', 'department', 'Department']
    for col in category_columns:
        if col in row.index and pd.notna(row[col]):
            info['category'] = str(row[col])
            break
    
    # Get SKU/Barcode
    sku_columns = ['sku', 'SKU', 'barcode', 'Barcode', 'product_id', 'Product ID']
    for col in sku_columns:
        if col in row.index and pd.notna(row[col]):
            info['sku'] = str(row[col])
            break
    
    # Get URL
    info['url'] = str(row[url_column])
    
    return info

# Header
st.markdown('<div class="main-header">URL Image Viewer</div>', unsafe_allow_html=True)
st.markdown("### Automatically display product images from Excel URLs")

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Excel File",
        type=['xlsx', 'xls', 'csv'],
        help="Upload file containing product URLs"
    )
    
    if uploaded_file:
        try:
            # Read file
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Loaded {len(df)} rows")
            
            # Column selection
            st.subheader("Column Settings")
            url_column = st.selectbox(
                "URL Column",
                df.columns,
                index=0,
                help="Select the column containing image URLs"
            )
            
            # Filter out empty URLs
            df_filtered = df[df[url_column].notna()].copy()
            df_filtered = df_filtered[df_filtered[url_column].astype(str).str.strip() != '']
            
            if len(df_filtered) < len(df):
                st.warning(f"Filtered out {len(df) - len(df_filtered)} rows with empty URLs")
            
            st.session_state.df = df_filtered
            st.session_state.url_column = url_column
            
            # Display settings
            st.subheader("Display Settings")
            display_seconds = st.slider(
                "Display Time (seconds)",
                min_value=3,
                max_value=60,
                value=15,
                step=1,
                help="How long to display each image"
            )
            
            auto_advance = st.checkbox(
                "Auto-advance",
                value=False,
                help="Automatically move to next image after display time"
            )
            
            # Range selection
            st.subheader("Range Selection")
            total_items = len(df_filtered)
            
            col1, col2 = st.columns(2)
            with col1:
                start_index = st.number_input(
                    "Start at row",
                    min_value=1,
                    max_value=total_items,
                    value=1,
                    step=1
                ) - 1
            
            with col2:
                end_index = st.number_input(
                    "End at row",
                    min_value=1,
                    max_value=total_items,
                    value=min(10, total_items),
                    step=1
                )
            
            # Apply range
            st.session_state.df = df_filtered.iloc[start_index:end_index].reset_index(drop=True)
            
            st.info(f"Viewing {len(st.session_state.df)} items")
            
            # Preview data
            with st.expander("Preview Data"):
                st.dataframe(st.session_state.df.head(), use_container_width=True)
        
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
            st.session_state.df = None
    
    # Navigation info
    if st.session_state.df is not None:
        st.markdown("---")
        st.subheader("Navigation")
        st.info(f"Current: {st.session_state.current_index + 1} / {len(st.session_state.df)}")
        
        # History
        if st.session_state.viewing_history:
            with st.expander("Viewing History"):
                for item in st.session_state.viewing_history[-10:]:
                    st.caption(f"Row {item['index'] + 1}: {item['timestamp']}")

# Main content area
if st.session_state.df is not None and len(st.session_state.df) > 0:
    
    # Control buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("⏮️ First", use_container_width=True):
            st.session_state.current_index = 0
            st.rerun()
    
    with col2:
        if st.button("◀️ Previous", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.rerun()
    
    with col3:
        if auto_advance:
            if st.button("⏸️ Pause", use_container_width=True, type="primary"):
                st.session_state.auto_advance = False
                st.rerun()
        else:
            if st.button("▶️ Play", use_container_width=True, type="primary"):
                st.session_state.auto_advance = True
                st.rerun()
    
    with col4:
        if st.button("▶️ Next", use_container_width=True):
            if st.session_state.current_index < len(st.session_state.df) - 1:
                st.session_state.current_index += 1
                st.rerun()
    
    with col5:
        if st.button("⏭️ Last", use_container_width=True):
            st.session_state.current_index = len(st.session_state.df) - 1
            st.rerun()
    
    # Progress bar
    progress = (st.session_state.current_index + 1) / len(st.session_state.df)
    st.progress(progress)
    
    # Get current row
    current_row = st.session_state.df.iloc[st.session_state.current_index]
    product_info = get_product_info(current_row, st.session_state.url_column)
    
    # Display product information
    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### Product Image")
        
        # Image container
        image_placeholder = st.empty()
        
        # Load and display image
        with st.spinner(f"Loading image {st.session_state.current_index + 1}..."):
            img, error = load_image_from_url(product_info['url'])
            
            if img:
                # Display image
                image_placeholder.image(
                    img,
                    use_container_width=True,
                    caption=product_info.get('name', 'Product Image')
                )
                
                # Display description below image if available
                if 'description' in product_info:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                padding: 1.5rem; 
                                border-radius: 10px; 
                                margin-top: 1rem;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                        <p style='color: white; 
                                  margin: 0; 
                                  font-size: 1rem; 
                                  line-height: 1.6;
                                  font-weight: 500;'>
                            <strong style='font-size: 1.1rem;'>Description:</strong><br><br>
                            {product_info['description']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Log to history
                if not st.session_state.viewing_history or \
                   st.session_state.viewing_history[-1]['index'] != st.session_state.current_index:
                    st.session_state.viewing_history.append({
                        'index': st.session_state.current_index,
                        'timestamp': datetime.now().strftime("%H:%M:%S"),
                        'url': product_info['url']
                    })
            else:
                image_placeholder.error(f"Failed to load image: {error}")
                st.code(product_info['url'], language=None)
    
    with col_right:
        st.markdown("### Product Details")
        
        # Product information card
        info_html = '<div class="product-info">'
        
        if 'name' in product_info:
            info_html += f"<h4>{product_info['name']}</h4>"
        
        # Description - Make it prominent
        if 'description' in product_info:
            info_html += f"""
            <div style='background: #f0f2f6; padding: 1rem; border-radius: 8px; margin: 1rem 0; border-left: 4px solid #667eea;'>
                <p style='margin: 0; font-size: 0.95rem; line-height: 1.6; color: #262730;'>
                    <strong style='color: #667eea;'>Description:</strong><br>
                    {product_info['description']}
                </p>
            </div>
            """
        
        if 'sku' in product_info:
            info_html += f"<p><strong>SKU:</strong> {product_info['sku']}</p>"
        
        if 'price' in product_info:
            info_html += f"<p><strong>Price:</strong> {product_info['price']}</p>"
        
        if 'category' in product_info:
            info_html += f"<p><strong>Category:</strong> {product_info['category']}</p>"
        
        info_html += f'<p><strong>URL:</strong> <a href="{product_info["url"]}" target="_blank">Open in new tab</a></p>'
        info_html += '</div>'
        
        st.markdown(info_html, unsafe_allow_html=True)
        
        # Jump to specific row
        st.markdown("### Jump to Row")
        jump_to = st.number_input(
            "Row number",
            min_value=1,
            max_value=len(st.session_state.df),
            value=st.session_state.current_index + 1,
            key="jump_input"
        ) - 1
        
        if st.button("Go", use_container_width=True):
            st.session_state.current_index = jump_to
            st.rerun()
        
        # Download options
        # st.markdown("### 💾 Export")
        
        if img:
            # Convert PIL image to bytes
            buf = BytesIO()
            img.save(buf, format='PNG')
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Current Image",
                data=byte_im,
                file_name=f"product_{st.session_state.current_index + 1}.png",
                mime="image/png",
                use_container_width=True
            )
    
    # Auto-advance logic
    if auto_advance and st.session_state.current_index < len(st.session_state.df) - 1:
        # Countdown timer
        countdown_placeholder = st.empty()
        
        for remaining in range(display_seconds, 0, -1):
            countdown_placeholder.markdown(
                f'<div class="countdown">Next image in {remaining}s</div>',
                unsafe_allow_html=True
            )
            time.sleep(1)
        
        # Advance to next image
        st.session_state.current_index += 1
        countdown_placeholder.empty()
        st.rerun()
    
    elif auto_advance and st.session_state.current_index >= len(st.session_state.df) - 1:
        st.success("Reached the end of the slideshow!")
        st.session_state.auto_advance = False
        
        if st.button("Start Over"):
            st.session_state.current_index = 0
            st.session_state.auto_advance = True
            st.rerun()

else:
    # Welcome screen
    st.markdown("""
    <div style='text-align: center; padding: 3rem;'>
        <h2> URL Image Viewer</h2>
        <p style='font-size: 1.2rem; color: #666;'>
            Upload an Excel file 
        </p>
        <br>
    </div>
    """, unsafe_allow_html=True)
    
    # Example data format
#     with st.expander("📖 Example Excel Format"):
#         example_data = {
#             'url_1': [
#                 'https://example.com/image1.jpg',
#                 'https://example.com/image2.png',
#                 'https://example.com/image3.jpg'
#             ],
#             'product_name': ['Product A', 'Product B', 'Product C'],
#             'price': ['$19.99', '$29.99', '$39.99'],
#             'category': ['Electronics', 'Clothing', 'Home']
#         }
#         st.dataframe(pd.DataFrame(example_data), use_container_width=True)

# # Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    URL Image Viewer | Built with Streamlit
</div>
""", unsafe_allow_html=True)
