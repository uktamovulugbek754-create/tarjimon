# Tarjimon - Arab Tilidagi Audioni Ingliz Tiliga Dubbl Qilish Saytи

Bu loyiha Arab tilidagi audioni Ingliz tiliga tarjima qilib, dubbl audioni tayyorlaydi.

## Xususiyatlari

- 🎤 Arab tilidagi audio yuklash
- 🔄 Avtomatik tarjima (Arab → Ingliz)
- 🎧 Ingliz tilidagi dubbl audio tayyorlash
- 📱 Zamonaviy responsive interfeys

## Texnologiyalar

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python Flask
- **API**: Google Cloud Speech-to-Text, Translation API, Text-to-Speech

## O'rnatish

### Talablar

- Python 3.8+
- Node.js (opsional - frontend development uchun)
- Google Cloud API kalit

### Setup

1. Repozitoriyani clone qiling:
```bash
cd tarjimon
```

2. Virtual environment yarating:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Dependensiyalarni o'rnating:
```bash
pip install -r requirements.txt
```

4. Google Cloud credentials-ni o'rnating:
```bash
set GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

5. Serverni ishga tushiring:
```bash
python app.py
```

6. Brauzerda oching:
```
http://localhost:5000
```

## Fayllar Tuzilishi

```
tarjimon/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependensiyalari
├── static/
│   ├── css/
│   │   └── style.css     # Stillar
│   └── js/
│       └── script.js     # Frontend logic
├── templates/
│   └── index.html        # Asosiy sahifa
└── README.md
```

## Qo'llanma

1. **Audio yuklash**: "Faylni tanlash" tugmasini bosing
2. **Dubbl jarayoni**: Avtomatik ravishda boshlanadi
3. **Natija**: Dubbl qilingan audio yuklab oling

---
**Tarjimon** - Arab tilidagi audioni Ingliz tiliga dubbl qilish vositasi
