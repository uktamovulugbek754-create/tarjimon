# 🧪 Tarjimon - Test Qo'llanmasi

## 🚀 Tez Test Qilish

### 1. Demo Versiyasini Test Qilish

```bash
# Terminalda ishga tushiring
python app_demo.py

# Brauzerda oching
http://localhost:5000
```

**Test qiladigan narsa:**
- ✅ Upload bo'limi ko'rinadi
- ✅ Progress bar animatsiya ishlaydi
- ✅ Natija sahifasi ko'rinadi
- ✅ Audio player ishga tusadi

---

## 🔧 API Testing

### Health Check
```bash
curl http://localhost:5000/api/health
```

**Kutilgan javob:**
```json
{
  "status": "ok",
  "message": "Tarjimon API demo ishga tushdi"
}
```

### Audio Processing (Demo)
```bash
curl -X POST \
  -F "audio=@test_audio.mp3" \
  http://localhost:5000/api/process-audio
```

**Kutilgan javob:**
```json
{
  "success": true,
  "original_text": "As-salam alaikum wa rahmatullahi wa barakatuh",
  "translated_text": "Hello, peace and God's mercy and blessings be upon you",
  "audio_url": "/api/download-audio"
}
```

---

## 📝 Frontend Testing

### Upload Funksiyasi
1. Brauzer oching: `http://localhost:5000`
2. "Audio faylini shu yerga drag qiling" bo'limiga bosing
3. MP3 yoki WAV fayl tanlang
4. Fayl nomi va hajmi ko'rinadi?
   - ✅ Ko'rinadi
   - ❌ Ko'rinmadi - xato

### Dubbl Qilish Tugmasi
1. Audio faylini yuklang
2. "Dubbl Qilishni Boshlash" tugmasi aktiv bo'ladimi?
   - ✅ Bo'ladi
   - ❌ Bo'lmadi - xato

### Progress Animation
1. Tugmani bosing
2. Progres bar animatsiya qiladi?
   - ✅ Qiladi
   - ❌ Qilmadi - xato

### Natija Sahifasi
1. Asl matni ko'rinadi?
   - ✅ Ko'rinadi
   - ❌ Ko'rinmadi - xato
2. Tarjimosi ko'rinadi?
   - ✅ Ko'rinadi
   - ❌ Ko'rinmadi - xato
3. Audio player ko'rinadi?
   - ✅ Ko'rinadi
   - ❌ Ko'rinmadi - xato

---

## 🧬 Browser DevTools Testing

### Console
```javascript
// Terminalda:
console.log('API connection test');

// Brauzerni aching
F12 → Console tab
// Xatolar ko'rinadi?
```

### Network
1. F12 → Network tab
2. Audio yuklab olishni qayta qo'y
3. Requestlarni ko'ring:
   - POST /api/process-audio
   - GET /api/download-audio

### Performance
1. F12 → Performance tab
2. Audio ishlab chiqarish vaqti
3. CSS/JS load time

---

## 🐛 Debug Rejimi

### Flask Debug
```bash
# .env faylida
FLASK_DEBUG=True

# Serverga o'zgarish bo'lsa avtomatik reload qiladi
python app.py
```

### JavaScript Debug
```javascript
// Browser console-da
// Fayllarni tekshiring:
fetch('/api/health')
  .then(r => r.json())
  .then(d => console.log(d))
```

---

## 📊 Performance Testing

### Load Time
```bash
# DevTools Lighthouse ishlating
# F12 → Lighthouse → Analyze page load
```

### File Size
```bash
# Audio fayl hajmi
ls -lh uploads/

# HTML/CSS/JS hajmi
ls -lh static/
```

---

## 🎯 E2E Test Checklist

- [ ] Server ishga tushadi
- [ ] Ana sahifa yuklanadi
- [ ] Audio faylini yuklash ishlaydi
- [ ] Dubbl qilish boshlashni isserlaydi
- [ ] Progress bar animatsiya qiladi
- [ ] Natija sahifasi ko'rinadi
- [ ] Audio yuklab olish ishlaydi
- [ ] Reset tugmasi ishlaydi
- [ ] Xatolar to'g'rida ko'rsatiladi

---

## 🔍 Common Issues & Solutions

### Issue: Upload bo'limi ko'rinmadi
**Solution**: Browser cache tozalang (Ctrl+Shift+Delete)

### Issue: API 404 error beradi
**Solution**: Flask server ishga tushurilganmi, tekshiring

### Issue: Audio player ishlamadi
**Solution**: Browser audio support tekshiring (F12 → Console)

### Issue: Slow processing
**Solution**: Network speed tekshiring, fayl hajmi kichiklashtiring

---

## ✅ Production Testing Checklist

- [ ] SSL certificate o'rnatildi
- [ ] Error logging konfiguratsiyalandi
- [ ] Rate limiting o'rnatildi
- [ ] CORS sozlandi
- [ ] Security headers qo'shildi
- [ ] File upload virus check o'rnatildi
- [ ] Database backup avtomatik
- [ ] Monitoring setup qilindi
- [ ] Load testing o'tkazildi

---

## 📱 Mobile Testing

### iOS Safari
- [ ] Audio upload ishlaydi
- [ ] Progress bar ko'rinadi
- [ ] Natija display to'g'ri

### Android Chrome
- [ ] Audio upload ishlaydi
- [ ] Performance muammo yo'q
- [ ] Responsive layout to'g'ri

---

## 🚀 Load Testing

### Apache Bench
```bash
ab -n 100 -c 10 http://localhost:5000
```

### Wrk
```bash
wrk -t4 -c100 -d30s http://localhost:5000
```

---

## 📈 Metrics to Monitor

- Server response time
- CPU/Memory usage
- API request count
- Error rate
- File upload speed

---

**Test qilib, haqiqiy loyihaga tayyorlang! ✅**
