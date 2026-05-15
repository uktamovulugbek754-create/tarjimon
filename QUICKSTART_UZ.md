# 🎬 Tarjimon - Boshlang'ich Qo'llanma (O'zbek)

**Assalammualaikum! 👋**

Bu loyiha Arab tilidagi audioni Ingliz tiliga tarjima qilib, dubbl audio yaratadi.

---

## ⚡ 30 soniyada Boshlang'ich (Eng Tez)

```bash
# 1. Papkaga kirib, koding ishga tushiring
python app_demo.py

# 2. Brauzer oching
http://localhost:5000

# Done! ✅
```

---

## 📋 Talablar

- **Python 3.8+** - [Python yuklab olish](https://www.python.org/downloads/)
- **Text editor** - VS Code, PyCharm, yoki har qanday editor
- **Brauzerni** - Chrome, Firefox, Safari, Edge

### Qo'shimcha (Ixtiyoriy):
- Docker - Osonroq deployment uchun
- Git - Version control uchun

---

## 🚀 3 Ta Usuli Ishga Tushirish

### ✅ Usul 1: Demo (Eng Tez, Google Cloud kerak emas)

```bash
python app_demo.py
# → http://localhost:5000
```

**Orzularni**:
- Hechqanday setup kerak emas
- Demo ma'lumotlar bilan ishlaydi
- Frontend & API structure ko'rish uchun ideali

---

### ✅ Usul 2: Haqiqiy (Google Cloud API-lari bilan)

**1-qadam: Google Cloud Setup**

```bash
# https://console.cloud.google.com -ga o'ting
# 1. Yangi proyekt yarating
# 2. Quyidagi API-larni faollashtiring:
#    - Cloud Speech-to-Text
#    - Cloud Translation API
#    - Cloud Text-to-Speech
# 3. Service Account yarating
# 4. JSON kalit saqlang
```

**2-qadam: Python Setup**

```bash
# Virtual environment yarating
python -m venv venv

# Faollashtiring
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Dependensiyalarni o'rnating
pip install -r requirements.txt
```

**3-qadam: Credentials o'rnating**

```bash
# JSON faylini loyiha papkasiga joylashtiring
# credentials.json nomi bilan

# GOOGLE_APPLICATION_CREDENTIALS sozlang
# Windows:
set GOOGLE_APPLICATION_CREDENTIALS=credentials.json
# macOS/Linux:
export GOOGLE_APPLICATION_CREDENTIALS=credentials.json
```

**4-qadam: Ishga tushirish**

```bash
python app.py
```

---

### ✅ Usul 3: Docker (Tavsiya qilingan)

```bash
# Docker o'rnatish (agar o'rnatilmagan bo'lsa)
# https://www.docker.com/products/docker-desktop

# Ishga tushirish
docker-compose up

# Brauzerda:
# http://localhost:5000
```

---

## 🎯 Foydalanish

1. **Audio faylini yuklash**
   - "Faylni tanlash" bo'limiga bosing
   - MP3 yoki WAV formatda audio tanlang
   - 100MB gacha ruxsat

2. **Dubbl qilishni boshlash**
   - "Dubbl Qilishni Boshlash" tugmasini bosing
   - 3 ta qadamda amalga oshadi:
     - 🎤 Gaplarni aniqlash
     - 📝 Matni tarjima qilish
     - 🎧 Ingliz tilidagi audio yaratish

3. **Natijani yuklab olish**
   - Asl Arab matni ko'rish
   - Tarjimosi (Ingliz) ko'rish
   - Audio-ni ijro qilish
   - "Audiyo Yuklab Olish" tugmasini bosing

---

## 📂 Fayllar Struktura

```
tarjimon/
├── app.py                 ← Haqiqiy Flask app
├── app_demo.py           ← Demo app (o'rnatish kerak emas)
├── requirements.txt      ← Python paketlari
├── Dockerfile            ← Docker setup
├── docker-compose.yml    ← Docker Compose
│
├── templates/
│   └── index.html        ← Veb sahifa
├── static/
│   ├── css/style.css     ← Stil
│   └── js/script.js      ← Interaktivlik
│
└── README.md
    INSTALL.md
    QUICKSTART.md        ← Bu fayl
    TESTING.md
    DEVELOPMENT.md
    PROJECT_STRUCTURE.md
```

---

## 🔧 Muammo-Yechim

### ❌ "ModuleNotFoundError" xatosi

```bash
# Yechim:
pip install -r requirements.txt
```

### ❌ "Port 5000 already in use"

```bash
# Yechim: Boshqa port ishlatish
python app.py --port 8000
# http://localhost:8000
```

### ❌ Google Cloud xatosi

```bash
# Yechim:
set GOOGLE_APPLICATION_CREDENTIALS=credentials.json
python app.py
```

### ❌ Audio upload bo'lmadi

```
Tekshiring:
1. Audio format MP3 yoki WAV ekanligini
2. Fayl hajmi 100MB dan oshmasligi
3. Browser console-da (F12) xatolarni ko'ring
```

---

## 📚 Ko'p Ishlatilgan Buyruqlar

```bash
# Virtual environment yaratish
python -m venv venv

# Virtual environment-ni faollashtirish
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt

# Paketlarni yangilash
pip install --upgrade google-cloud-speech

# Flask app-ni ishga tushirish
python app.py

# Boshqa portda ishga tushirish
python app.py --port 8000

# Demo-ni ishga tushirish
python app_demo.py

# Docker-da ishga tushirish
docker-compose up

# Docker-ni to'xtatish
docker-compose down

# Logs ko'rish
docker-compose logs -f
```

---

## 🌐 URL-lar

- **Frontend**: http://localhost:5000
- **API Health**: http://localhost:5000/api/health
- **API Docs**: http://localhost:5000/api/docs (agar Swagger qo'shilgan bo'lsa)

---

## 🎓 Keyingi Qadamlar

1. ✅ Demo-ni test qiling
2. ✅ Google Cloud account yarating
3. ✅ Haqiqiy app-ni o'rnating
4. ✅ Turli til-paridagi audio fayllarini test qiling
5. ✅ Frontend-ni moslang (qo'shimcha xususiyatlar qo'shing)
6. ✅ Database qo'shing (history saqlash uchun)
7. ✅ User authentication qo'shing
8. ✅ Production-ga deploy qiling

---

## 💡 Foydali Manbalar

| Mabao | Link |
|------|------|
| Python | https://www.python.org |
| Flask | https://flask.palletsprojects.com |
| Google Cloud | https://cloud.google.com |
| Docker | https://www.docker.com |
| VS Code | https://code.visualstudio.com |

---

## 🆘 Yordam Kerakmi?

1. **INSTALL.md** - Batafsil o'rnatish
2. **TESTING.md** - Test qilish
3. **DEVELOPMENT.md** - Ustun o'zgartirishlar
4. **PROJECT_STRUCTURE.md** - Fayllar haqqida

---

## ✨ Features

- ✅ Modern, responsive UI
- ✅ Drag & drop audio upload
- ✅ Real-time progress tracking
- ✅ Arabic speech recognition
- ✅ Text translation
- ✅ English dubbed audio
- ✅ Download dubbed audio
- ✅ Error handling
- ✅ Mobile friendly
- ✅ Dark mode support

---

## 🚀 Production Uchun

```bash
# Environment o'zgaruvchisini sozlang
set FLASK_ENV=production

# WSGI server ishlatish (Gunicorn)
pip install gunicorn
gunicorn -w 4 app:app

# Nginx konfiguratsiyasini sozlang
# SSL certificate qo'shing (Let's Encrypt)
# Backup system setup qiling
# Monitoring setup qiling
```

---

## 🎉 Hammasi Tayyor!

Veb-sayt:
- ✅ Frontend - HTML/CSS/JS
- ✅ Backend - Flask + Google Cloud
- ✅ Deploy - Docker ready
- ✅ Dokumentatsiya - O'zbek tilidagi qo'llanmalar
- ✅ Testing - Test guide
- ✅ Development - Extension guide

**Ishga Tush!** 🚀

---

**Savollar bo'lsa, dokumentatsiyani ko'ring yoki GitHub Issues oching.**

**Muaffaqiyat!** 🎊
