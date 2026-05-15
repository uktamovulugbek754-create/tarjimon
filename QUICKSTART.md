# 🚀 Tez Boshlash

## Demo Versiyasini Tezda Ishga Tushirish (Google Cloud kerak emas)

```bash
# 1. Virtual environment yarating
python -m venv venv

# 2. Faollashtiring
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Dependensiyalarni o'rnating
pip install Flask

# 4. Demo serverni ishga tushiring
python app_demo.py
```

Keyin brauzerda oching: **http://localhost:5000**

---

## Haqiqiy Google Cloud API-lari bilan

### Ishlash Tartibi:

1. **Google Cloud Account Yaratish**
   ```
   https://console.cloud.google.com
   ```

2. **API-larni Faollashtirish**
   - Cloud Speech-to-Text
   - Cloud Translation API
   - Cloud Text-to-Speech

3. **Service Account Yaratish**
   - Service Account yarating
   - JSON kalit saqlang

4. **Credentials Sozlash**
   ```bash
   set GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
   ```

5. **Haqiqiy App-ni Ishga Tushirish**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

---

## Docker-da Ishga Tushirish

```bash
# Build image
docker build -t tarjimon .

# Run container
docker run -p 5000:5000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
  tarjimon
```

Yoki docker-compose bilan:

```bash
docker-compose up
```

---

## 🎯 Vazifalar

- [ ] Demo-ni test qiling
- [ ] Google Cloud account yarating
- [ ] API-larni faollashtiring
- [ ] Credentials saqlang
- [ ] Haqiqiy app-ni ishga tushiring
- [ ] Audio faylini test qiling

---

## 📞 Savol/Muammolar?

- [INSTALL.md](INSTALL.md) - Batafsil o'rnatish qo'llanmasi
- [README.md](README.md) - Loyiha haqida
- GitHub Issues - Muammolar va taklif uchun

---

**Muvaffaqiyat! 🎉**
