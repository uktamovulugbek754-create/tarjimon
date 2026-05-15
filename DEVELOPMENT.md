# 👨‍💻 Tarjimon - Development Qo'llanmasi

## 🏗️ Arhitektura

```
┌─────────────────────────────────────────────────┐
│             User Browser (Frontend)              │
│  ┌────────────────────────────────────────────┐ │
│  │  HTML (index.html)                         │ │
│  │  ├─ Upload Area                            │ │
│  │  ├─ Progress Section                       │ │
│  │  └─ Results Section                        │ │
│  │                                             │ │
│  │  CSS (style.css) - Styling & Responsive   │ │
│  │  JS (script.js) - Event handling & API     │ │
│  └────────────────────────────────────────────┘ │
└─────────────┬──────────────────────────────────┘
              │ HTTP/AJAX
              ↓
┌─────────────────────────────────────────────────┐
│           Flask Backend (Python)                 │
│  ┌────────────────────────────────────────────┐ │
│  │  app.py (Main Server)                      │ │
│  │  ├─ /                   (GET)  → index.html│ │
│  │  ├─ /api/health         (GET)  → Status   │ │
│  │  ├─ /api/process-audio  (POST) → Process  │ │
│  │  └─ /api/download-audio (GET)  → Download │ │
│  │                                             │ │
│  │  Functions:                                 │ │
│  │  ├─ recognize_speech_arabic()              │ │
│  │  ├─ translate_text()                       │ │
│  │  └─ synthesize_speech_english()            │ │
│  └────────────────────────────────────────────┘ │
└─────────────┬──────────────────────────────────┘
              │ API Calls
              ↓
┌─────────────────────────────────────────────────┐
│        Google Cloud APIs                         │
│  ├─ Speech-to-Text (Arabic)                     │
│  ├─ Translation API (AR → EN)                   │
│  └─ Text-to-Speech (English)                    │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Ustun O'zgartirishlar

### 1. Boshqa Tili Qo'shish

**app.py-da:**
```python
def recognize_speech_custom(audio_path, language_code):
    """
    Custom language support
    """
    config = speech_v1.RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,  # "ar-SA", "en-US", "fr-FR", etc.
    )
    # ... rest of code
```

**HTML-da:**
```html
<select id="languageSelect">
    <option value="ar-SA">العربية (Arabic)</option>
    <option value="en-US">English</option>
    <option value="fr-FR">Français</option>
    <option value="de-DE">Deutsch</option>
</select>
```

### 2. Audio Samarjohot Qilish

```python
from pydub import AudioSegment

def process_audio_quality(input_path, output_path):
    """Audio samarjohot qilish"""
    audio = AudioSegment.from_mp3(input_path)
    
    # Volume o'zgartirish
    audio = audio + 6  # +6 dB
    
    # Export
    audio.export(output_path, format="mp3", bitrate="192k")
```

### 3. Caching Qo'shish

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/process-audio', methods=['POST'])
@cache.cached(timeout=3600)
def process_audio():
    # Cached response
    pass
```

### 4. Database Qo'shish (History)

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarjimon.db'
db = SQLAlchemy(app)

class ProcessingHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String(1000))
    translated_text = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    language_pair = db.Column(db.String(20))
```

### 5. User Authentication Qo'shish

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager(app)

@app.route('/api/process-audio', methods=['POST'])
@login_required
def process_audio():
    # Protected endpoint
    pass
```

---

## 🧩 File Structure O'zgartirish

### Modular Backend Tuzish

```python
# api/speech.py
from google.cloud import speech_v1

def recognize_speech(audio_path, language):
    # Speech recognition logic
    pass

# api/translate.py
from google.cloud import translate_v2

def translate(text, source, target):
    # Translation logic
    pass

# api/tts.py
from google.cloud import texttospeech_v1

def synthesize(text, language, voice):
    # TTS logic
    pass

# app.py
from api import speech, translate, tts

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    arabic_text = speech.recognize_speech(audio, 'ar-SA')
    english_text = translate.translate(arabic_text, 'ar', 'en')
    output = tts.synthesize(english_text, 'en-US', 'neural2-c')
```

---

## 🌐 Frontend Features

### Real-time Progress Updates

```javascript
const eventSource = new EventSource('/api/process-audio-stream');

eventSource.addEventListener('progress', (e) => {
    console.log(e.data); // {"step": 1, "progress": 50}
});
```

### Drag & Drop Improvement

```javascript
document.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
});
```

### Service Worker (Offline Support)

```javascript
// static/js/sw.js
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('tarjimon-v1').then((cache) => {
            return cache.addAll([
                '/',
                '/static/css/style.css',
                '/static/js/script.js'
            ]);
        })
    );
});
```

---

## 🧪 Testing Framework Qo'shish

### Pytest

```python
# tests/test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_process_audio(client):
    # Test audio processing
    pass
```

---

## 🚀 Performance Optimization

### Compression

```python
from flask_compress import Compress

Compress(app)
```

### CORS

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Async Processing

```python
from celery import Celery

celery = Celery(app.name)

@celery.task
def process_audio_async(audio_path):
    # Long-running task
    pass

# In route
task = process_audio_async.delay(audio_path)
```

---

## 📊 Analytics Qo'shish

```python
from flask_analytics import Analytics

analytics = Analytics(app)

# Track events
@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    analytics.track_event('audio_processing', {
        'language': 'ar-SA',
        'file_size': file.size
    })
```

---

## 🔐 Security Improvements

```python
# Helmet-like headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

---

## 🐳 Docker Multi-Stage Build

```dockerfile
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local:$PATH
CMD ["python", "app.py"]
```

---

## 📝 Code Style

### Black Formatting

```bash
black app.py
```

### Linting

```bash
flake8 app.py
pylint app.py
```

### Type Hints

```python
from typing import Optional, Dict

def process_audio(audio_path: str) -> Dict[str, str]:
    """Process audio file and return translations."""
    pass
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

---

## 📚 API Documentation

### Swagger/OpenAPI

```python
from flasgger import Swagger

swagger = Swagger(app)

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """
    Process Arabic audio to English dubbed audio
    ---
    parameters:
      - name: audio
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Success
    """
    pass
```

---

## 🎓 Debugging Tips

1. **Flask Debug Toolbar**
   ```python
   from flask_debugtoolbar import DebugToolbarExtension
   toolbar = DebugToolbarExtension(app)
   ```

2. **Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   logger = logging.getLogger(__name__)
   ```

3. **Breakpoints**
   ```python
   import pdb; pdb.set_trace()
   ```

---

## 🚀 Deployment Tahqiqlash

- [ ] Environment variables sozlandi
- [ ] Database migrated
- [ ] Static files collected
- [ ] Logs configured
- [ ] Monitoring setup
- [ ] SSL certificates installed
- [ ] Backup system ready
- [ ] Rollback plan ready

---

**Happy Coding! 🎉**
