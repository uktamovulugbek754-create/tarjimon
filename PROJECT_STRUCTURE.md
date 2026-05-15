# 📋 Tarjimon - Loyiha Ichidagi Fayllar

## 📂 Tuzilish

```
tarjimon/
├── app.py                    # Haqiqiy Flask app (Google Cloud API-lari)
├── app_demo.py              # Demo Flask app (o'rnatish kerak emas)
├── config.py                # Konfiguratsiya sozlamalari
│
├── requirements.txt         # Python dependensiyalari
├── requirements-dev.txt     # Development dependensiyalari
│
├── Dockerfile              # Docker containerization
├── docker-compose.yml      # Docker Compose konfiguratsiyasi
│
├── .env.example           # Environment o'zgaruvchilari namunasi
├── .gitignore             # Git ignoring qoidalari
│
├── README.md              # Loyiha haqida (O'zbek)
├── INSTALL.md             # O'rnatish qo'llanmasi (O'zbek)
├── QUICKSTART.md          # Tez boshlash (O'zbek)
│
├── static/
│   ├── css/
│   │   └── style.css      # Veb sayt stillar (CSS)
│   └── js/
│       └── script.js      # Frontend JavaScript
│
└── templates/
    └── index.html         # Asosiy HTML sahifa
```

---

## 📝 Fayllar Tavsifi

### Backend Fayllar

| Fayl | Maqsad |
|------|--------|
| `app.py` | Haqiqiy app - Google Cloud Speech-to-Text, Translate, Text-to-Speech API-larini qo'llaydi |
| `app_demo.py` | Demo app - o'rnatish kerak emas, tezda test qilish uchun |
| `config.py` | Konfiguratsiya o'zgaruvchilari |
| `requirements.txt` | Asosiy Python paketlari |
| `requirements-dev.txt` | Development uchun qo'shimcha paketlari |

### Frontend Fayllar

| Fayl | Maqsad |
|------|--------|
| `templates/index.html` | Asosiy veb sahifa (HTML) |
| `static/css/style.css` | Dizayn va layout (CSS) |
| `static/js/script.js` | Interaktivlik va API chaqiruvlar (JavaScript) |

### Konfiguratsiya Fayllar

| Fayl | Maqsad |
|------|--------|
| `.env.example` | Environment o'zgaruvchilari namunasi |
| `.gitignore` | Git uchun ignoring qoidalari |
| `Dockerfile` | Docker container setup |
| `docker-compose.yml` | Multi-container setup |

### Dokumentatsiya

| Fayl | Maqsad |
|------|--------|
| `README.md` | Loyiha tavsifi va xususiyatlari |
| `INSTALL.md` | Batafsil o'rnatish qo'llanmasi |
| `QUICKSTART.md` | Tez boshlash bo'yicha qo'llanma |

---

## 🔧 Ishga Tushirish Variantlari

### 1. Demo (Eng Tez)
```bash
python app_demo.py
# Google Cloud kerak emas!
# http://localhost:5000
```

### 2. Haqiqiy (Google Cloud bilan)
```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Google Cloud credentials o'rnating
set GOOGLE_APPLICATION_CREDENTIALS=credentials.json

# Ishga tushiring
python app.py
```

### 3. Docker (Tavsiya qilingan)
```bash
docker-compose up
```

---

## 🌟 Asosiy Xususiyatlari

✅ **Dizayn**: Modern, responsive UI  
✅ **Speech Recognition**: Arab tilidagi audioni matnga aylantirish  
✅ **Tarjima**: Arab matni Ingliz tiliga tarjima qilish  
✅ **Text-to-Speech**: Ingliz matni shodani audioga aylantirish  
✅ **Upload/Download**: Fayllarni yuklash va yuklab olish  
✅ **Progress Tracking**: Real-time jarayon kuzatish  
✅ **Error Handling**: Xatolarni batafsil ko'rsatish  

---

## 📊 API Endpoints

| Endpoint | Metod | Maqsad |
|----------|-------|--------|
| `/` | GET | Asosiy sahifa |
| `/api/health` | GET | Server faolligini tekshirish |
| `/api/process-audio` | POST | Audio faylini dubbl qilish |
| `/api/download-audio` | GET | Natijani yuklab olish |

---

## 💻 Technology Stack

**Frontend:**
- HTML5
- CSS3 (Responsive Design)
- JavaScript (Vanilla - Framework-less)

**Backend:**
- Python 3.8+
- Flask (Web Framework)
- Google Cloud APIs
  - Speech-to-Text
  - Translation API
  - Text-to-Speech

**DevOps:**
- Docker
- Docker Compose

---

## 🎯 Qo'llash Ketma-Ketligi

1. **Audio yuklash** - User MP3/WAV faylini yuklaydi
2. **Aniqlash** - Google Speech-to-Text Arab matni ajratib oladi
3. **Tarjima** - Google Translate Arab matni Ingliz tiliga tarjima qiladi
4. **Synthesize** - Google Text-to-Speech Ingliz matni shodani audio qiladi
5. **Natija** - Dubbl qilingan audio user-ga qaytariladi

---

## 🔐 Xavfsizlik

- ✅ File size limit: 100MB
- ✅ File type validation
- ✅ CSRF protection ready
- ✅ Google Cloud credentials encrypted
- ✅ Input sanitization

---

## 📱 Browser Qo'llab-quvvatlash

- ✅ Chrome/Edge (v90+)
- ✅ Firefox (v88+)
- ✅ Safari (v14+)
- ✅ Mobile Browsers

---

## 🆘 Troubleshooting

### Muammo: "Module not found" xatosi
**Yechim**: `pip install -r requirements.txt`

### Muammo: Port 5000 band
**Yechim**: `python app.py --port 8000`

### Muammo: Google Cloud xatosi
**Yechim**: `.env` faylida `GOOGLE_APPLICATION_CREDENTIALS` sozlang

---

## 📚 Foydali Manbalar

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [HTML/CSS/JS MDN](https://developer.mozilla.org/)

---

**Tayyor! Veb-sayt to'liq ishga tayinlangan. 🚀**
