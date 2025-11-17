# 🇮🇳 AI Product Price Finder - India

An AI-powered web application that identifies products from images and compares prices across major Indian e-commerce platforms.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Table of Contents
- [About](#about)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Supported Platforms](#supported-platforms)
- [Project Information](#project-information)
- [Screenshots](#screenshots)
- [Disclaimer](#disclaimer)
- [License](#license)

---

## 📖 About

This project uses advanced AI vision models to identify products from images and provides intelligent price estimates across popular Indian e-commerce platforms. Built with Streamlit and powered by Groq's Llama models.

---

## ✨ Features

### 🎯 Smart Product Identification
- AI-powered product recognition using Llama 4 Scout Vision
- Automatic brand and model detection
- Category classification
- Feature extraction from images

### 💰 Price Comparison
- Multi-platform price comparison
- Best deal highlighting
- Savings calculator
- Price analytics dashboard

### 🇮🇳 India-Focused
- Prices in Indian Rupees (INR)
- Major Indian e-commerce platforms
- Card discounts and offers
- COD and EMI information
- Festival sale awareness

### 📸 Multiple Input Methods
- Camera capture support
- Image file upload (JPG, PNG, WEBP)
- Manual product search option

---

## 🛠 Technology Stack

| Component | Technology |
|-----------|-----------|
| *Frontend* | Streamlit |
| *AI Vision* | Groq API - Llama 4 Scout (17B) |
| *AI Analysis* | Groq API - Llama 3.3 (70B) |
| *Image Processing* | Pillow (PIL) |
| *HTTP Requests* | Requests library |
| *Language* | Python 3.8+ |

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Steps

1. *Clone the repository*
```bash
git clone https://github.com/YOUR_USERNAME/ai-product-price-finder.git
cd ai-product-price-finder
Create virtual environment (recommended)
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
Install dependencies
pip install -r requirements.txt
Set up configuration
mkdir .streamlit
Create .streamlit/secrets.toml file with:
GROQ_API_KEY = "your_groq_api_key_here"
