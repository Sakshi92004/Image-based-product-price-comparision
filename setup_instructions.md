# Setup Instructions

## 🔑 Getting Groq API Key

### Step-by-Step Guide

1. *Visit Groq Console*
   - Go to [https://console.groq.com](https://console.groq.com)

2. *Create Account*
   - Click on "Sign Up" button
   - Use your email or Google account
   - Verify your email if required

3. *Generate API Key*
   - Once logged in, navigate to "API Keys" section
   - Click on "Create API Key" button
   - Give your key a name (e.g., "Product Price Finder")
   - Copy the generated API key immediately (you won't see it again!)

4. *Save Your API Key*
   - Keep it secure
   - Never share it publicly
   - Never commit it to GitHub

---

## ⚙ Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-product-price-finder.git
cd ai-product-price-finder
2. Create Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate
macOS/Linux:
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure API Key
Create .streamlit folder:
mkdir .streamlit
Create secrets.toml file:
Create a file at .streamlit/secrets.toml with the following content:
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
Replace gsk_your_actual_groq_api_key_here with your actual API key from Groq.
Example:
GROQ_API_KEY = "gsk_abc123xyz456def789ghi012jkl345mno678"
🚀 Running the Application
Start the App
streamlit run main.py
What to Expect
Streamlit will start a local server
Your default browser will open automatically
URL: http://localhost:8501
If browser doesn't open, manually visit the URL
First Time Setup
Allow camera permissions (if using camera feature)
Test with a product image
Check if API key is working correctly
🧪 Testing the App
Test 1: Image Upload
Go to "Upload Image" tab
Upload a clear product image
Click "Identify Product & Find Prices"
Verify product identification works
Test 2: Manual Search
Scroll to "Manual Product Search"
Enter: "iPhone 15 Pro"
Click "Search Prices Manually"
Check price results
Test 3: Camera Capture
Go to "Take Photo" tab
Allow camera access
Take a photo of any product
Verify identification
❌ Troubleshooting
Problem: "GROQ_API_KEY not found"
Solution:
Check if .streamlit/secrets.toml file exists
Verify the file is in the correct location
Ensure the API key is properly formatted
Restart the Streamlit app
Problem: "Module not found"
Solution:
pip install -r requirements.txt
Problem: Camera not working
Solution:
Check browser permissions
Try different browser (Chrome recommended)
Ensure HTTPS or localhost
Problem: "API Error 401"
Solution:
Your API key is invalid or expired
Generate new key from Groq Console
Update .streamlit/secrets.toml
Problem: "API Error 429"
Solution:
You've exceeded rate limits
Wait a few minutes
Check Groq Console for usage limits
📁 File Structure
ai-product-price-finder/
│
├── main.py                          # Main application file
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
├── LICENSE                          # MIT License
├── setup_instructions.md            # This file
├── .gitignore                       # Git ignore rules
│
└── .streamlit/                      # Streamlit configuration
    └── secrets.toml                 # API keys (NOT in GitHub)
🔒 Security Best Practices
✅ DO:
Keep API keys in .streamlit/secrets.toml
Add secrets.toml to .gitignore
Use environment variables in production
Regularly rotate API keys
❌ DON'T:
Commit API keys to GitHub
Share API keys publicly
Hardcode keys in source code
Post keys in issues or PRs
🌐 Deployment (Optional)
Deploying to Streamlit Cloud
Push code to GitHub (without secrets.toml)
Go to share.streamlit.io
Connect your GitHub repository
Add GROQ_API_KEY in Streamlit Cloud secrets
Deploy!
Environment Variables in Streamlit Cloud
In Streamlit Cloud dashboard:
GROQ_API_KEY = "your_key_here"
📞 Support
If you encounter issues:
Check this setup guide thoroughly
Review error messages carefully
Check Groq API status
Verify all dependencies are installed
✅ Setup Checklist
[ ] Python 3.8+ installed
[ ] Repository cloned
[ ] Virtual environment created
[ ] Dependencies installed
[ ] Groq API key obtained
[ ] .streamlit/secrets.toml created
[ ] API key added to secrets.toml
[ ] App runs successfully
[ ] Image upload works
[ ] Product identification works
[ ] Price comparison works
