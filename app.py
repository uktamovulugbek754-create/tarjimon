# ============================================================
# Tarjimon Pro — Arabic-to-English Dubbing API
# Pipeline: Whisper (timestamps) → DeepL → Edge TTS (timed) → mix with original
# ============================================================

from flask import Flask, render_template, request, jsonify, send_file
from groq import Groq
import deepl
import edge_tts
from dotenv import load_dotenv
import os
import asyncio
import shutil
from pathlib import Path

load_dotenv()

# ── App setup ────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))

app.config['MAX_CONTENT_LENGTH'] = 400 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ── API keys ──────────────────────────────────────────────────
GROQ_API_KEY      = os.environ.get("GROQ_API_KEY")
DEEPL_API_KEY     = os.environ.get("DEEPL_API_KEY")
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.webm', '.flv', '.wmv', '.m4v'}

# Har bir notiqqa alohida ovoz (speaker 1→4)
SPEAKER_VOICES = [
    "en-US-GuyNeural",          # Notiq 1 — erkak
    "en-US-ChristopherNeural",  # Notiq 2 — erkak
    "en-US-EricNeural",         # Notiq 3 — erkak
    "en-US-RogerNeural",        # Notiq 4 — erkak
]

# Tarjima qilinmaydigan arabcha iboralar
PRESERVE_PHRASES = [
    ('الله أكبر',        'Allahu Akbar'),
    ('اللَّه أكبر',      'Allahu Akbar'),
    ('اللّٰه أكبر',      'Allahu Akbar'),
    ('سبحان الله',       'Subhanallah'),
    ('سبحانه وتعالى',    'Subhanahu wa Ta\'ala'),
    ('الحمد لله',        'Alhamdulillah'),
    ('لا إله إلا الله',  'La ilaha illallah'),
    ('لا اله الا الله',  'La ilaha illallah'),
    ('إن شاء الله',      "Insha'Allah"),
    ('ان شاء الله',      "Insha'Allah"),
    ('بسم الله',         'Bismillah'),
    ('ما شاء الله',      "Masha'Allah"),
    ('ماشاء الله',       "Masha'Allah"),
    ('أشهد أن',          'Ashhadu an'),
    ('صلى الله عليه',    'Sallallahu alayhi'),
    ('رضي الله عنه',     'Radiyallahu anhu'),
]


def get_groq_client():
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY topilmadi.")
    return Groq(api_key=GROQ_API_KEY)


# ── Routes ────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    missing = [k for k, v in {
        'GROQ_API_KEY':      GROQ_API_KEY,
        'DEEPL_API_KEY':     DEEPL_API_KEY,
        'HUGGINGFACE_TOKEN': HUGGINGFACE_TOKEN,
    }.items() if not v]
    if missing:
        return jsonify({'status': 'warning', 'message': f'Missing keys: {", ".join(missing)}'}), 200
    return jsonify({'status': 'ok', 'message': 'Tarjimon Pro API ishlayapti'}), 200


@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """
    Pipeline:
      1. (Video) ffmpeg → audio
      2. Notiqlarni aniqlash (LLM orqali)
      3a. Groq Whisper — avtomatik transkripsiya  (txt yuklanmagan bo'lsa)
      3b. txt fayl — qo'lda transkripsiya         (txt yuklanganida Whisper o'tkazib yuboriladi)
      4. DeepL — har bir segment tarjima
      5. Edge TTS — har bir segmentni to'g'ri vaqtga joylashtirish
      6. pydub — dubbed audio + original audio (past volume) aralashtiriladi
      7. (Video) ffmpeg — dubbed audio videoga qaytariladi
    """
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Audio/video fayl kiritilmagan'}), 400

        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'Fayl tanlanmagan'}), 400

        ext      = Path(audio_file.filename).suffix.lower() or '.mp3'
        is_video = ext in VIDEO_EXTENSIONS

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f'input{ext}')
        audio_file.save(upload_path)

        # ── Step 1: Audio tayyorlash ──────────────────────────
        if is_video:
            try:
                audio_for_pipeline = extract_audio_from_video(upload_path)
            except Exception as e:
                return jsonify({'error': f'Videodan audio ajratib bo\'lmadi: {e}'}), 500
        else:
            try:
                audio_for_pipeline = compress_audio(upload_path)
            except Exception:
                audio_for_pipeline = upload_path

        num_speakers = 1

        # ── Step 3: Transkripsiya (txt yoki Whisper) ──────────
        txt_file = request.files.get('transcript')
        used_manual_transcript = False

        if txt_file and txt_file.filename.endswith('.txt'):
            txt_path = os.path.join(app.config['UPLOAD_FOLDER'], 'transcript.txt')
            txt_file.save(txt_path)
            segments, formatted_arabic = parse_transcript_file(txt_path)
            used_manual_transcript = True
            if not segments:
                return jsonify({'error': 'Transkripsiya fayli bo\'sh yoki noto\'g\'ri formatda.'}), 400
        else:
            if not GROQ_API_KEY:
                return jsonify({'error': 'GROQ_API_KEY sozlanmagan. Transkripsiya txt faylini yuklang yoki API kalitni qo\'shing.'}), 500
            segments, formatted_arabic = transcribe_with_timestamps(audio_for_pipeline)
            if not segments:
                return jsonify({'error': 'Audio matnini aniqlab bo\'lmadi. Audio sifatini tekshiring.'}), 400

        # ── Step 2b: Notiqlarni matn orqali aniqlash ─────────
        try:
            num_speakers = detect_speakers_from_text(segments)
        except Exception as e:
            print(f"[Speaker detection] skipped: {e}")

        # ── Step 3b: Har bir segmentga notiq raqami berish ───
        speaker_labels = assign_speakers(segments, num_speakers)
        for i, seg in enumerate(segments):
            seg['speaker'] = speaker_labels[i] if i < len(speaker_labels) else 1

        # ── Step 4: Tarjima ───────────────────────────────────
        translated_segments = translate_segments(segments)
        formatted_english = format_segments(translated_segments, use_translated=True)

        if not any(s.get('translated') for s in translated_segments):
            return jsonify({'error': 'Matnni tarjima qilib bo\'lmadi'}), 400

        # ── Step 5: Timed TTS synthesis ───────────────────────
        total_ms = int(translated_segments[-1]['end'] * 1000) + 2000
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            dubbed_path = loop.run_until_complete(
                synthesize_timed_speech(translated_segments, total_ms)
            )
        finally:
            loop.close()

        if not dubbed_path:
            return jsonify({'error': 'Inglizcha audio yaratib bo\'lmadi'}), 400

        # ── Step 6: Mix dubbed + original audio ───────────────
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_audio.mp3')
        try:
            mix_dubbed_with_original(dubbed_path, audio_for_pipeline, output_path)
        except Exception as e:
            print(f"[Step 6] Mix skipped: {e}")
            shutil.copy(dubbed_path, output_path)

        # ── Step 7: (Video) merge audio back ──────────────────
        if is_video:
            video_output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_video.mp4')
            try:
                merge_audio_into_video(upload_path, output_path, video_output_path)
            except Exception as e:
                print(f"[Step 7] Video merge failed: {e}")
                is_video = False

        return jsonify({
            'success':                True,
            'original_text':          formatted_arabic,
            'translated_text':        formatted_english,
            'num_speakers':           num_speakers,
            'is_video':               is_video,
            'used_manual_transcript': used_manual_transcript,
            'audio_url':              '/api/download-audio',
            'video_url':              '/api/download-video' if is_video else None,
        }), 200

    except Exception as e:
        print(f"[process_audio] Xato: {e}")
        return jsonify({'error': str(e)}), 500


# ── Helpers ───────────────────────────────────────────────────

def _fmt_time(seconds):
    """121.4 → '2:01'"""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"


def parse_transcript_file(txt_path):
    """
    Qo'lda yozilgan transkripsiya txt faylini o'qiydi.

    Qo'llab-quvvatlanadigan formatlar:
      A) "0:00 Arabcha matn"   — timestamp va matn bir qatorda (bo'sh joy bilan yoki bo'lmay)
      B) Timestamp alohida qatorda, keyin arabcha matn alohida qatorda:
           0:08
           8 seconds
           وقتها قوم لوت...
    "8 seconds", "2 minutes, 30 seconds" kabi inglizcha tavsiflar o'tkazib yuboriladi.
    """
    import re

    def is_arabic(text):
        return bool(re.search(r'[؀-ۿ]', text))

    def parse_time(ts):
        parts = ts.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])

    with open(txt_path, 'r', encoding='utf-8-sig') as f:
        raw_lines = [ln.strip() for ln in f.read().splitlines()]

    entries = []          # (start_sec, time_label, arabic_text)
    cur_time  = None
    cur_label = None
    pending   = []        # arabcha matn parchalar

    for line in raw_lines:
        if not line:
            continue

        # Timestamp bor qatormi? (boshida M:SS yoki H:MM:SS)
        m = re.match(r'^(\d+:\d{2}(?::\d{2})?)(.*)', line)
        if m:
            # Oldingi segmentni saqlash
            if cur_time is not None and pending:
                entries.append((cur_time, cur_label, ' '.join(pending).strip()))
            cur_time  = parse_time(m.group(1))
            cur_label = m.group(1)
            pending   = []
            rest = m.group(2).strip()
            # Timestamp bilan birga arabcha matn bor bo'lsa
            if rest and is_arabic(rest):
                pending.append(rest)
        else:
            # Arabcha matn qatori
            if is_arabic(line) and cur_time is not None:
                pending.append(line)
            # "8 seconds", "2 minutes, 30 seconds" kabilar — o'tkazib yuboriladi

    # Oxirgi entry
    if cur_time is not None and pending:
        entries.append((cur_time, cur_label, ' '.join(pending).strip()))

    if not entries:
        return None, None

    segments  = []
    formatted = []
    for i, (start, label, text) in enumerate(entries):
        end = entries[i + 1][0] if i + 1 < len(entries) else start + 5
        if end <= start:
            end = start + 3
        segments.append({
            'start':      float(start),
            'end':        float(end),
            'text':       text,
            'time_label': label,
        })
        formatted.append(f"{label} {text}")

    return segments, "\n".join(formatted)


def transcribe_with_timestamps(audio_path):
    """
    Groq Whisper verbose_json — har bir segment uchun start/end vaqt qaytaradi.
    Natija: (segments list, formatlangan arabcha matn)
    """
    try:
        groq_client = get_groq_client()
        with open(audio_path, 'rb') as f:
            result = groq_client.audio.transcriptions.create(
                file=(os.path.basename(audio_path), f.read()),
                model="whisper-large-v3",
                language="ar",
                response_format="verbose_json"
            )

        segments = []
        lines    = []
        for seg in result.segments:
            text = (seg.get('text') or '').strip()
            if not text:
                continue
            start = seg.get('start') or 0
            end   = seg.get('end')   or start
            segments.append({
                'start': start,
                'end':   end,
                'text':  text,
                'time_label': _fmt_time(start),
            })
            lines.append(f"{_fmt_time(start)} {text}")

        if not segments:
            return None, None

        return segments, "\n".join(lines)

    except Exception as e:
        print(f"[transcribe_with_timestamps] Xato: {e}")
        return None, None


def _protect_phrases(text):
    placeholders = {}
    result = text
    for i, (phrase, keep_as) in enumerate(PRESERVE_PHRASES):
        if phrase in result:
            token = f'__KEEP{i}__'
            placeholders[token] = keep_as
            result = result.replace(phrase, f' {token} ')
    return result, placeholders


def _restore_phrases(text, placeholders):
    for token, phrase in placeholders.items():
        text = text.replace(token, phrase)
    return text


def translate_arabic_to_english(text):
    try:
        protected, placeholders = _protect_phrases(text)

        if DEEPL_API_KEY:
            translator = deepl.Translator(DEEPL_API_KEY)
            result     = translator.translate_text(protected, source_lang="AR", target_lang="EN-US")
            translated = result.text
        else:
            from deep_translator import GoogleTranslator
            translated = GoogleTranslator(source='ar', target='en').translate(protected)
            if not translated:
                return None

        return _restore_phrases(translated, placeholders)
    except Exception as e:
        print(f"[translate] Xato: {e}")
        return None


def translate_segments(segments):
    """
    Barcha segmentlarni BITTA API chaqiruvida tarjima qiladi (batch).
    200 ta segment = 200 chaqiruv emas, 1 ta chaqiruv.
    """
    if not segments:
        return []

    # Har bir matnni himoya qilamiz
    protected_list   = []
    placeholder_list = []
    for seg in segments:
        p, ph = _protect_phrases(seg['text'])
        protected_list.append(p)
        placeholder_list.append(ph)

    # Batch tarjima
    translated_list = []
    try:
        if DEEPL_API_KEY:
            translator = deepl.Translator(DEEPL_API_KEY)
            results    = translator.translate_text(
                protected_list, source_lang="AR", target_lang="EN-US"
            )
            translated_list = [
                _restore_phrases(r.text, ph)
                for r, ph in zip(results, placeholder_list)
            ]
        else:
            # Google Translate fallback — bittabittadan (batch yo'q)
            from deep_translator import GoogleTranslator
            gt = GoogleTranslator(source='ar', target='en')
            for pt, ph in zip(protected_list, placeholder_list):
                t = gt.translate(pt) or ''
                translated_list.append(_restore_phrases(t, ph))
    except Exception as e:
        print(f"[translate_segments] Batch xato: {e}")
        translated_list = [''] * len(segments)

    result = []
    for i, seg in enumerate(segments):
        result.append({
            'start':      seg['start'],
            'end':        seg['end'],
            'original':   seg['text'],
            'translated': translated_list[i] if i < len(translated_list) else '',
            'time_label': seg['time_label'],
            'speaker':    seg.get('speaker', 1),
        })
    return result


def format_segments(segments, use_translated=False):
    """Segmentlarni '0:00 matn' formatida birlashtiradi."""
    lines = []
    for seg in segments:
        text = seg['translated'] if use_translated else seg['original']
        if text:
            lines.append(f"{seg['time_label']} {text}")
    return "\n".join(lines)


async def synthesize_timed_speech(segments, total_ms):
    """
    Har bir segment uchun Edge TTS audio yaratadi va
    to'g'ri timestamp pozitsiyasiga joylashtiradi.
    """
    from pydub import AudioSegment as AS
    try:
        base = AS.silent(duration=max(total_ms, 2000))

        for i, seg in enumerate(segments):
            text = seg.get('translated', '').strip()
            if not text:
                continue

            # Notiq raqamiga qarab ovoz tanlanadi (1-indeksli, 0-indeksli list)
            voice_idx = (seg.get('speaker', 1) - 1) % len(SPEAKER_VOICES)
            voice     = SPEAKER_VOICES[voice_idx]
            communicate = edge_tts.Communicate(text, voice)
            tmp = os.path.join(app.config['UPLOAD_FOLDER'], f'_seg_{i}.mp3')
            await communicate.save(tmp)

            seg_audio = AS.from_file(tmp)
            try:
                os.remove(tmp)
            except Exception:
                pass

            pos = int(seg['start'] * 1000)
            base = base.overlay(seg_audio, position=pos)

        out = os.path.join(app.config['UPLOAD_FOLDER'], 'dubbed_speech.mp3')
        base.export(out, format='mp3')
        return out

    except Exception as e:
        print(f"[synthesize_timed_speech] Xato: {e}")
        return None


def mix_dubbed_with_original(dubbed_path, original_path, output_path, orig_db=-30):
    """
    Dubbed nutqni original audio bilan aralаshtiradi.
    Original audio -18 dB ga tushiriladi (background sifatida qoladi).
    """
    from pydub import AudioSegment
    dubbed   = AudioSegment.from_file(dubbed_path)
    original = AudioSegment.from_file(original_path) + orig_db

    if len(original) < len(dubbed):
        loops    = (len(dubbed) // len(original)) + 1
        original = original * loops
    original = original[:len(dubbed)]

    dubbed.overlay(original).export(output_path, format='mp3')


def compress_audio(audio_path):
    """Audio faylni Groq uchun 16kHz mono 24kbps MP3 ga aylantiradi."""
    import subprocess
    out = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.mp3')
    subprocess.run(
        ['ffmpeg', '-y', '-i', audio_path,
         '-vn', '-acodec', 'libmp3lame', '-ar', '16000', '-ac', '1', '-b:a', '24k',
         out],
        check=True, capture_output=True, text=True
    )
    return out


def extract_audio_from_video(video_path):
    """
    ffmpeg: video → 16kHz mono MP3.
    24kbps saqlaydi — 30 daqiqa ~5MB, Groq 25MB chegarasidan ancha past.
    """
    import subprocess
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_audio.mp3')
    subprocess.run(
        ['ffmpeg', '-y', '-i', video_path,
         '-vn', '-acodec', 'libmp3lame', '-ar', '16000', '-ac', '1', '-b:a', '24k',
         audio_path],
        check=True, capture_output=True, text=True
    )
    return audio_path


def merge_audio_into_video(video_path, audio_path, output_path):
    """ffmpeg: original video rasm + dubbed audio → MP4."""
    import subprocess
    subprocess.run(
        ['ffmpeg', '-y',
         '-i', video_path,
         '-i', audio_path,
         '-c:v', 'copy',
         '-map', '0:v:0',
         '-map', '1:a:0',
         '-shortest',
         output_path],
        check=True, capture_output=True, text=True
    )


def detect_speakers_from_text(segments):
    """
    Groq LLM yordamida transkripsiya segmentlarini tahlil qilib
    nechta notiq borligini aniqlaydi. PyTorch shart emas.
    """
    try:
        client = get_groq_client()
        # Birinchi 40 segmentni olamiz (haddan oshmasligi uchun)
        sample = segments[:40]
        text   = "\n".join(f"{s['time_label']} {s['text']}" for s in sample)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{
                "role": "system",
                "content": (
                    "You are an audio analyst. Analyze the Arabic transcript and count "
                    "how many distinct speakers are present. Look for: conversational patterns "
                    "(questions and answers), different people being addressed, dialogue markers, "
                    "topic shifts that indicate speaker change. "
                    "Respond with ONLY a single integer number."
                )
            }, {
                "role": "user",
                "content": f"How many distinct speakers are in this transcript?\n\n{text}"
            }],
            max_tokens=5,
            temperature=0,
        )
        count = int(response.choices[0].message.content.strip().split()[0])
        return max(1, min(count, 20))
    except Exception as e:
        print(f"[detect_speakers_from_text] Xato: {e}")
        return 1


def assign_speakers(segments, num_speakers):
    """
    Groq LLM yordamida har bir segmentga notiq raqami (1..num_speakers) beradi.
    Natija: segments uzunligidagi int ro'yxati.
    """
    if num_speakers <= 1:
        return [1] * len(segments)
    try:
        client  = get_groq_client()
        sample  = segments[:60]
        lines   = "\n".join(f"{i}: {s['time_label']} {s['text']}" for i, s in enumerate(sample))

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        f"You are analyzing an Arabic transcript. There are exactly {num_speakers} speakers. "
                        f"Assign a speaker number (1 to {num_speakers}) to each numbered line. "
                        "Use conversational context (questions, answers, who is being addressed). "
                        "Return ONLY a JSON array of integers, one per line. "
                        f"Example for 3 lines with 2 speakers: [1, 2, 1]"
                    ),
                },
                {
                    "role": "user",
                    "content": f"Assign speaker numbers to each line:\n{lines}",
                },
            ],
            max_tokens=600,
            temperature=0,
        )

        import json, re
        content = resp.choices[0].message.content.strip()
        match   = re.search(r'\[[\d,\s]+\]', content)
        if match:
            labels = json.loads(match.group())
            result = []
            for i in range(len(segments)):
                lbl = labels[i] if i < len(labels) else 1
                result.append(max(1, min(int(lbl), num_speakers)))
            return result
    except Exception as e:
        print(f"[assign_speakers] Xato: {e}")
    return [1] * len(segments)


def detect_speakers(audio_path):
    from pyannote.audio import Pipeline
    pipeline    = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token=HUGGINGFACE_TOKEN
    )
    diarization = pipeline(audio_path)
    speakers    = {speaker for _, _, speaker in diarization.itertracks(yield_label=True)}
    return len(speakers), diarization


def mix_audio(speech_path, background_path, output_path, bg_volume_db=-12):
    from pydub import AudioSegment
    speech     = AudioSegment.from_file(speech_path)
    background = AudioSegment.from_file(background_path) + bg_volume_db
    if len(background) < len(speech):
        background = background * ((len(speech) // len(background)) + 1)
    background = background[:len(speech)]
    speech.overlay(background).export(output_path, format='mp3')


# ── Download endpoints ────────────────────────────────────────

@app.route('/api/download-audio')
def download_audio():
    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_audio.mp3')
        if not os.path.exists(path):
            return jsonify({'error': 'Audio fayl topilmadi'}), 404
        return send_file(path, mimetype='audio/mpeg', as_attachment=True,
                         download_name='tarjimon_output.mp3')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download-video')
def download_video():
    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_video.mp4')
        if not os.path.exists(path):
            return jsonify({'error': 'Video fayl topilmadi'}), 404
        return send_file(path, mimetype='video/mp4', as_attachment=True,
                         download_name='tarjimon_output.mp4')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Error handlers ────────────────────────────────────────────

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Topilmadi'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server xatosi'}), 500


# ── Entry point ───────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
