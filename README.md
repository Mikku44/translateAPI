# Khain Translate API  
**Open-Source Translation Service with Self-Hosted AI Models**  

![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)  
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green)  

## 📌 Overview  
Khain is an open-source translation API that enables:  
✅ **100+ language pairs** using Facebook's M2M100 model  
✅ **Self-hostable** with Docker support  
✅ **Enterprise-ready** with rate limiting and monitoring  
✅ **MIT/Apache licensed** - Commercially friendly  

## 🚀 Features  
- Powered by state-of-the-art **M2M100-418M** model  
- **Low latency** (<500ms per request)  
- **No API keys** required for self-hosted instances  
- Supports **batch translation**  
- Built with **FastAPI** for high performance  

## 🛠️ Installation  

### Option 1: Docker (Recommended)  
```bash 
docker build -t khain-translate .  
docker run -p 8000:8000 khain-translate

git clone https://github.com/yourrepo/khain-translate.git
cd khain-translate
pip install -r requirements.txt
uvicorn main:app --reload
```

```{
  "text": "Hello world",
  "source_lang": "en",
  "target_lang": "th"
}```
