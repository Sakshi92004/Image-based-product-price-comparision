import streamlit as st
import requests
from PIL import Image
import io
import base64
from datetime import datetime
import json
import re

# Page configuration
st.set_page_config(
    page_title="AI Product Price Finder - India",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .product-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f9f9f9;
    }
    .price-tag {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2ecc71;
    }
    .retailer-name {
        font-size: 1.2rem;
        color: #34495e;
        font-weight: 600;
    }
    .best-deal {
        background-color: #d5f4e6;
        border: 2px solid #27ae60;
    }
    .upload-section {
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    .stButton>button {
        width: 100%;
    }
    .indian-flag {
        background: linear-gradient(to bottom, #FF9933 33%, white 33%, white 66%, #138808 66%);
        padding: 2px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'product_name' not in st.session_state:
    st.session_state.product_name = None
if 'identified_product' not in st.session_state:
    st.session_state.identified_product = None

def image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffered = io.BytesIO()
    if image.mode in ('RGBA', 'LA', 'P'):
        image = image.convert('RGB')
    image.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode()

def identify_product_from_image(image):
    """
    Use Groq API with Llama 4 Scout vision model to identify product
    """
    text_content = ""
    try:
        with st.spinner("🤖 Analyzing image with AI..."):
            base64_image = image_to_base64(image)
            
            # Get API key from Streamlit secrets
            api_key = st.secrets.get("GROQ_API_KEY", None)
            if not api_key:
                st.error("⚠️ GROQ_API_KEY not found. Please add it to .streamlit/secrets.toml")
                st.code("""
# Create .streamlit/secrets.toml with:
GROQ_API_KEY = "gsk_your-groq-api-key-here"
                """)
                return None
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json={
                    "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": """Analyze this product image carefully and identify what it is. Be as specific as possible about brand, model, and features.

Return ONLY a valid JSON object with no additional text, explanations, or markdown:
{
    "product_name": "specific product name with brand and model if visible",
    "brand": "brand name",
    "category": "product category (electronics/fashion/home/etc)",
    "description": "brief description of visible features",
    "search_query": "optimized search query for Indian e-commerce sites"
}

Important: Return ONLY the JSON object, nothing else."""
                                }
                            ]
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 1024
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                text_content = data['choices'][0]['message']['content']
                
                # Clean and extract JSON
                text_content = text_content.strip()
                
                # Remove markdown if present
                if '```json' in text_content:
                    start = text_content.find('```json') + 7
                    end = text_content.find('```', start)
                    if end == -1:
                        end = len(text_content)
                    text_content = text_content[start:end].strip()
                elif '```' in text_content:
                    start = text_content.find('```') + 3
                    end = text_content.find('```', start)
                    if end == -1:
                        end = len(text_content)
                    text_content = text_content[start:end].strip()
                
                # Find JSON object
                json_start = text_content.find('{')
                json_end = text_content.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = text_content[json_start:json_end]
                    product_info = json.loads(json_str)
                    return product_info
                else:
                    st.error("Could not find valid JSON in response")
                    with st.expander("View raw response"):
                        st.text_area("Raw Response", text_content, height=200)
                    return None
            else:
                st.error(f"Groq API Error: {response.status_code}")
                with st.expander("View error details"):
                    st.code(response.text)
                return None
                
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {str(e)}")
        with st.expander("View raw response"):
            st.text_area("Raw Response", text_content, height=200)
        return None
    except Exception as e:
        st.error(f"Error identifying product: {str(e)}")
        return None

def search_product_prices_groq(product_query):
    """
    Use Groq API to generate search strategy and provide price estimates
    Note: Groq doesn't have built-in web search, so this provides intelligent estimates
    """
    try:
        with st.spinner(f"🔍 Analyzing prices for: {product_query}..."):
            api_key = st.secrets.get("GROQ_API_KEY", None)
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are an expert on Indian e-commerce pricing. Provide realistic price estimates based on your knowledge of the Indian market. Focus on these platforms: Amazon India, Flipkart, Myntra, Ajio, Meesho, Snapdeal.

Important: 
1. All prices must be in Indian Rupees (INR)
2. Consider Indian market conditions and pricing
3. Include typical discounts and offers
4. Be realistic about availability
5. Return ONLY valid JSON, no explanations"""
                        },
                        {
                            "role": "user",
                            "content": f"""Based on your knowledge of Indian e-commerce, provide typical current prices for: {product_query}

List at least 5 major Indian retailers with realistic price estimates.

Return ONLY a JSON array with NO other text, explanations, or markdown:
[
  {{
    "retailer": "Amazon India",
    "price": 89999,
    "condition": "new",
    "url": "https://amazon.in",
    "availability": "typically in stock",
    "discount": "10% off on HDFC cards"
  }}
]

Remember:
- Prices in INR (Indian Rupees)
- Include Amazon India, Flipkart, Myntra, Ajio, Meesho
- Realistic Indian market prices
- Common payment offers (card discounts, EMI, COD)
- Return ONLY JSON array, nothing else"""
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2048
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                full_text = data['choices'][0]['message']['content']
                
                # Clean and extract JSON
                clean_text = full_text.strip()
                
                # Remove markdown if present
                if '```json' in clean_text:
                    start = clean_text.find('```json') + 7
                    end = clean_text.find('```', start)
                    if end == -1:
                        end = len(clean_text)
                    clean_text = clean_text[start:end]
                elif '```' in clean_text:
                    start = clean_text.find('```') + 3
                    end = clean_text.find('```', start)
                    if end == -1:
                        end = len(clean_text)
                    clean_text = clean_text[start:end]
                
                # Find JSON array
                json_start = clean_text.find('[')
                json_end = clean_text.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = clean_text[json_start:json_end]
                    retailers = json.loads(json_str)
                    
                    if retailers and len(retailers) > 0:
                        return {
                            "product_name": product_query,
                            "search_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "retailers": retailers,
                            "raw_response": full_text,
                            "note": "⚠️ Prices are AI estimates based on market knowledge. Please verify on actual websites before purchasing."
                        }
                
                st.warning("⚠️ Could not parse price data")
                with st.expander("View response"):
                    st.text_area("Response", full_text, height=300)
                return None
            else:
                st.error(f"Groq API Error: {response.status_code}")
                with st.expander("View error details"):
                    st.code(response.text)
                return None
                
    except json.JSONDecodeError as e:
        st.error(f"Error parsing JSON: {str(e)}")
        with st.expander("View raw response"):
            st.text_area("Raw Response", full_text if 'full_text' in locals() else "No content", height=300)
        return None
    except Exception as e:
        st.error(f"Error searching prices: {str(e)}")
        return None

def display_product_info(product_info):
    """Display identified product information"""
    st.success("✅ Product Identified!")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 📦 Product Details")
        st.write(f"**Name:** {product_info.get('product_name', 'Unknown')}")
        st.write(f"**Brand:** {product_info.get('brand', 'Unknown')}")
        st.write(f"**Category:** {product_info.get('category', 'Unknown')}")
    
    with col2:
        st.markdown("### 📝 Description")
        st.write(product_info.get('description', 'No description available'))

def display_price_results(results):
    """Display price comparison results"""
    if not results or not results.get('retailers'):
        st.warning("⚠️ No price data found.")
        return
    
    # Show disclaimer for AI estimates
    if results.get('note'):
        st.info(results['note'])
    
    st.markdown(f"### 💰 Price Comparison for: {results['product_name']}")
    st.caption(f"Last updated: {results['search_date']}")
    
    retailers = results['retailers']
    valid_retailers = [r for r in retailers if r.get('price') and r['price'] > 0]
    
    if not valid_retailers:
        st.warning("No valid prices found.")
        return
    
    # Sort by price
    valid_retailers.sort(key=lambda x: x['price'])
    
    # Display results
    for idx, retailer in enumerate(valid_retailers):
        is_best = (idx == 0)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            icon = "🏆 " if is_best else ""
            st.markdown(f"{icon}**{retailer['retailer']}**")
            condition_text = f"{retailer.get('condition', 'New')} • {retailer.get('availability', 'Check availability')}"
            if retailer.get('discount'):
                condition_text += f" • 🎁 {retailer['discount']}"
            st.caption(condition_text)
        
        with col2:
            price_color = "#27ae60" if is_best else "#2ecc71"
            st.markdown(f"<span style='font-size:1.5rem;font-weight:bold;color:{price_color}'>₹{retailer['price']:,.0f}</span>", unsafe_allow_html=True)
        
        with col3:
            if retailer.get('url'):
                st.link_button("Visit Store", retailer['url'], use_container_width=True)
        
        st.divider()
    
    # Analytics
    st.markdown("### 📊 Price Analytics")
    col1, col2, col3, col4 = st.columns(4)
    
    prices = [r['price'] for r in valid_retailers]
    
    with col1:
        st.metric("Lowest Price", f"₹{min(prices):,.0f}")
    with col2:
        st.metric("Highest Price", f"₹{max(prices):,.0f}")
    with col3:
        st.metric("Average Price", f"₹{sum(prices)/len(prices):,.0f}")
    with col4:
        savings = max(prices) - min(prices)
        st.metric("Potential Savings", f"₹{savings:,.0f}", delta=f"-{(savings/max(prices)*100):.1f}%", delta_color="inverse")

# Main App UI
st.markdown('<div class="main-header">🇮🇳 AI Product Price Finder - India</div>', unsafe_allow_html=True)
st.markdown("**Upload a product image to find the best prices across Indian e-commerce platforms**")

# Important Notice
st.info("💡 **Powered by Groq AI** - This app uses Llama 4 Scout for product identification and provides intelligent price estimates. For real-time prices, always verify on the retailer's website.")

# Image Input Section
tab1, tab2 = st.tabs(["📷 Take Photo", "📁 Upload Image"])

uploaded_image = None

with tab1:
    st.info("📸 Allow camera access when prompted")
    camera_photo = st.camera_input("Take a picture of the product")
    if camera_photo:
        uploaded_image = Image.open(camera_photo)

with tab2:
    uploaded_file = st.file_uploader(
        "Choose a product image",
        type=['jpg', 'jpeg', 'png', 'webp'],
        help="Upload a clear photo of the product"
    )
    if uploaded_file:
        uploaded_image = Image.open(uploaded_file)

# Process uploaded image
if uploaded_image:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(uploaded_image, caption="Your Product", use_container_width=True)
    
    with col2:
        if st.button("🔍 Identify Product & Find Prices", type="primary", use_container_width=True):
            # Step 1: Identify product
            product_info = identify_product_from_image(uploaded_image)
            
            if product_info:
                st.session_state.identified_product = product_info
                display_product_info(product_info)
                
                # Step 2: Search for prices
                search_query = product_info.get('search_query') or product_info.get('product_name')
                
                if search_query:
                    st.markdown("---")
                    price_results = search_product_prices_groq(search_query)
                    
                    if price_results:
                        st.session_state.search_results = price_results
                        display_price_results(price_results)
            else:
                st.error("❌ Could not identify the product. Please try with a clearer image.")

# Manual Search Section
st.markdown("---")
st.markdown("### 🔤 Manual Product Search")
st.caption("Know the product name? Search directly:")

manual_query = st.text_input(
    "Enter product name:",
    placeholder="e.g., Samsung Galaxy S23 Ultra, Nike Air Max Shoes, Sony WH-1000XM5"
)

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("Search Prices Manually", use_container_width=True):
        if manual_query:
            price_results = search_product_prices_groq(manual_query)
            if price_results:
                st.session_state.search_results = price_results
                display_price_results(price_results)
        else:
            st.warning("Please enter a product name")

with col2:
    if st.button("Clear Results", use_container_width=True):
        st.session_state.search_results = None
        st.session_state.identified_product = None
        st.rerun()

# Show previous results if available
if st.session_state.search_results and not uploaded_image and not manual_query:
    st.markdown("---")
    st.markdown("### 📋 Previous Search Results")
    display_price_results(st.session_state.search_results)

# Supported Platforms Section
st.markdown("---")
st.markdown("### 🛒 Supported Indian E-commerce Platforms")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown("**🟠 Amazon India**")
    st.caption("amazon.in")
with col2:
    st.markdown("**🔵 Flipkart**")
    st.caption("flipkart.com")
with col3:
    st.markdown("**🟣 Myntra**")
    st.caption("myntra.com")
with col4:
    st.markdown("**🔴 Ajio**")
    st.caption("ajio.com")
with col5:
    st.markdown("**🟢 Meesho**")
    st.caption("meesho.com")

# Features Section
st.markdown("---")
st.markdown("### ✨ Features")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **🎯 Smart Identification**
    - AI-powered product recognition
    - Brand & model detection
    - Category classification
    - Feature extraction
    """)

with col2:
    st.markdown("""
    **💰 Price Intelligence**
    - Multi-platform comparison
    - Best deal highlighting
    - Savings calculation
    - Discount tracking
    """)

with col3:
    st.markdown("""
    **🇮🇳 India-Focused**
    - INR currency support
    - Indian platforms
    - Festival sale awareness
    - COD & EMI info
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 20px;'>
    <p>🔒 <strong>Privacy First:</strong> Images are processed securely and never stored</p>
    <p>⚡ Powered by Groq AI (Llama 4 Scout Vision + Llama 3.3 70B)</p>
    <p>🇮🇳 <strong>Made for India:</strong> Amazon India, Flipkart, Meesho, Ajio, Myntra</p>
    <p>💡 <strong>Tip:</strong> Use clear, well-lit photos for best results</p>
    <p>⚠️ <strong>Disclaimer:</strong> Prices are AI estimates. Always verify on retailer websites.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with info
with st.sidebar:
    st.markdown("## About This App")
    st.markdown("""
    This AI-powered app helps you find the best prices for products across Indian e-commerce platforms.
    
    ### How it works:
    1. **Upload/Capture** a product image
    2. **AI identifies** the product
    3. **Compare prices** across platforms
    4. **Find best deals** instantly
    
    ### Technology:
    - **Groq API** for fast AI inference
    - **Llama 4 Scout** for vision
    - **Llama 3.3 70B** for analysis
    - **Streamlit** for interface
    
    ### Supported Platforms:
    - 🟠 Amazon India
    - 🔵 Flipkart
    - 🟣 Myntra
    - 🔴 Ajio
    - 🟢 Meesho
    - 🟡 Snapdeal
    
    ### Payment Options Tracked:
    - 💳 Card discounts
    - 📱 UPI cashback
    - 💰 COD availability
    - 📊 EMI options
    
    ---
    
    **Project by:** Nikhil K (3GN23CD031)  
    **Guide:** Prof. Syed Saqlain Ahmed  
    **Institution:** GNDEC Bidar
    """)
    
    st.markdown("---")
    st.markdown("### Quick Tips")
    st.info("""
    📸 **Best Photo Practices:**
    - Good lighting
    - Clear brand logo
    - Straight angle
    - No reflections
    - Focus on product
    """)
    
    st.markdown("---")
    st.markdown("### API Setup")
    with st.expander("How to get Groq API Key"):
        st.markdown("""
        1. Visit [console.groq.com](https://console.groq.com)
        2. Sign up for free account
        3. Generate API key
        4. Add to `.streamlit/secrets.toml`:
        ```toml
        GROQ_API_KEY = "gsk_your_key_here"
        ```
        """)