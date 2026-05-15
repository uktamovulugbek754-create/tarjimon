# Tarjimon O'rnatish va Sozlash Qo'llanmasi

## 📋 Talablar

- **Python 3.8 yoki undan yuqori versiya**
- **Google Cloud Account** (bepul shartlar mavjud)
- **Windows, macOS yoki Linux**

## 🚀 Qadamlar

### 1. Google Cloud Loyiha Yaratish

1. [Google Cloud Console](https://console.cloud.google.com) ga o'ting
2. Yangi loyiha yarating
3. Quyidagi API-larni faollashtiring:
   - **Cloud Speech-to-Text API**
   - **Cloud Translation API**
   - **Cloud Text-to-Speech API**

### 2. Credentials Yaratish

1. Google Cloud Console-da:
   - Chap menyu → "APIs & Services" → "Credentials"
   - "Create Credentials" → "Service Account"
   - Xizmat hisobini yarating (har qanday nomi bo'ladi)
   - "Create and continue" ni bosing
   - "Create JSON key" ni tanlang
   - JSON fayl o'z kompyuteringizga saqlaning

2. JSON faylini proyekt papkasiga joylashtiring:
   ```
   tarjimon/
   ├── credentials.json  ← Shu yerga
   ├── app.py
   └── ...
   ```

### 3. Python Environment O'rnatish

**Windows:**
```powershell
# Virtual environment yarating
python -m venv venv

# Faollashtiring
venv\Scripts\activate

# Dependensiyalarni o'rnating
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Virtual environment yarating
python3 -m venv venv

# Faollashtiring
source venv/bin/activate

# Dependensiyalarni o'rnating
pip install -r requirements.txt
```

### 4. Environment O'zgaruvchisini Sozlash

**.env file yarating:**
```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

**.env faylini tahrirlang:**
```
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
FLASK_ENV=development
FLASK_DEBUG=True
```

### 5. Serverni Ishga Tushirish

```bash
python app.py
```

Brauzerda oching: **http://localhost:5000**

---

## 🔧 Mas'uliyatlash

### Muammolar va Yechimlar

#### "GOOGLE_APPLICATION_CREDENTIALS not set" xatosi

**Yechim:**
```bash
# Windows
set GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
python app.py

# macOS/Linux
export GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
python app.py
```

#### "ModuleNotFoundError: No module named 'google'" xatosi

**Yechim:**
```bash
# Virtual environment faol ekanligini tekshiring
pip install --upgrade google-cloud-speech google-cloud-translate google-cloud-texttospeech
```

#### Audio ishlab chiqarilishda xatolar

**Tekshiradigan narsalar:**
1. Google Cloud API-lar faolashtirilganmi?
2. Credentials.json to'g'rimi joylashtiriganmi?
3. API quotalari to'ldirilganmi?

---

## 📱 Foydalanish

1. **Audio Faylini Yuklash**
   - Brauzerda audio faylini tanlang
   - MP3, WAV, OGG formatlar qabul qilinadi
   - Maksimal 100MB

2. **Dubbl Qilishni Boshlash**
   - "Dubbl Qilishni Boshlash" tugmasini bosing
   - Jarayon 3 qadamda amalga oshadi:
     - Gaplarni aniqlash (Speech-to-Text)
     - Matni tarjima qilish (Translate)
     - Ingliz tilidagi audio yaratish (Text-to-Speech)

3. **Natijani Yuklab Olish**
   - Tarjimosi metnini ko'ring
   - Audio-ni ijro qiling
   - "Audiyo Yuklab Olish" tugmasini bosing

---

## 💰 Xarajatlari

### Google Cloud Narxlari (taxminiy)

- **Speech-to-Text**: $0.024 - $0.048 soat uchun
- **Translation**: $15 / 1 million belgiga
- **Text-to-Speech**: $4 - $16 / 1 million belgiga

### Bepul Shartlar (har oyda)

- Speech-to-Text: 60 daqiqa
- Translation: 500,000 belgigacha
- Text-to-Speech: 1 million belgigacha

---

## 🐛 Debug Rejimi

Loyihani debug rejimida ishga tushirish uchun:

```bash
# .env faylida
FLASK_DEBUG=True

# Keyin
python app.py
```

Server avtomatik ravishda qayta yuklanadi o'zgarishlar bo'lganda.

---

## 📚 Foydali Havolalar

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python-3.8+](https://www.python.org/downloads/)

---

## 🆘 Muammolar

Agar muammo yuz bersa, quyidagilarni tekshiring:

1. **Python versiyasi**: `python --version` (3.8+ bo'lishi kerak)
2. **Virtual environment**: Faol ekanligini tekshiring
3. **Dependencies**: `pip list` bilan tekshiring
4. **Google Cloud**: Credentials va API-lar to'g'rimi ekanligini tekshiring
5. **Port**: 5000-port band emasligini tekshiring

---

## 📞 Qo'llab-quvvatlash

Savol yoki muammolar bo'lsa, GitHub Issues-ni oching.

---

**Muvaffaqiyat!** 🎉
