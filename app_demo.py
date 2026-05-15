"""
Tarjimon - Demo Version (without Google Cloud)
This is a simplified demo for testing the UI and workflow.
In production, replace these functions with real Google Cloud API calls.
"""

import flask
from werkzeug.utils import secure_filename
import os
import uuid
import shutil
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = flask.Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Demo data - in production, use actual Google Cloud APIs
DEMO_TRANSLATIONS = {
    'as-salam alaikum': 'Hello, peace be upon you',
    'sabah al-khair': 'Good morning',
    'shukran': 'Thank you',
    'min fadlak': 'Please',
    'aywa': 'Yes',
    'la': 'No',
    'ana assif': 'I am sorry',
}

@app.route('/')
def index():
    """Main page"""
    return flask.render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return flask.jsonify({'status': 'ok', 'message': 'Tarjimon API demo ishga tushdi'}), 200

@app.route('/api/process-audio', methods=['POST'])
def process_audio():
    """
    Demo endpoint - simulates audio processing
    In production: 1. Speech-to-text 2. Translate 3. Text-to-speech
    """
    try:
        if 'audio' not in flask.request.files:
            return flask.jsonify({'error': 'Audio file not provided'}), 400
        
        audio_file = flask.request.files['audio']
        
        if audio_file.filename == '':
            return flask.jsonify({'error': 'No file selected'}), 400
        
        # Save uploaded file with unique name
        input_filename = secure_filename(audio_file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], f'input_{uuid.uuid4()}_{input_filename}')
        audio_file.save(upload_path)
        
        print(f"✓ Audio yuklandi: {input_filename} ({os.path.getsize(upload_path)} bytes)")
        
        # Demo: Generate fake Arabic and English text
        # In production, use Google Cloud Speech-to-Text
        arabic_text = "As-salam alaikum wa rahmatullahi wa barakatuh"
        english_text = "Hello, peace and God's mercy and blessings be upon you"
        
        print(f"✓ Arab matni: {arabic_text}")
        print(f"✓ Tarjimosi: {english_text}")
        
        # Demo: Copy uploaded file to output (simulate dubbing)
        # In production, use Google Cloud Text-to-Speech
        output_audio_path = copy_as_output_audio(upload_path)
        
        response_data = {
            'success': True,
            'original_text': arabic_text,
            'translated_text': english_text,
            'audio_url': '/api/download-audio'
        }
        
        print(f"✓ API javob tayyoq: {response_data}")
        
        return flask.jsonify(response_data), 200
    
    except Exception as e:
        error_msg = f"❌ Xato: {str(e)}"
        print(error_msg)
        return flask.jsonify({'error': str(e)}), 500

def copy_as_output_audio(input_path):
    """Copy uploaded audio as output (demo - simulates dubbing)"""
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_audio.mp3')
    
    try:
        # Copy the input file to output
        shutil.copy2(input_path, output_path)
        output_size = os.path.getsize(output_path)
        print(f"✓ Audio ko'chirildi: {output_size} bytes")
        return output_path
    except Exception as e:
        print(f"⚠ Copy xatosi: {str(e)}, alternativ usul bilan harakat qilyapman...")
        # If copy fails, try to read and write
        try:
            with open(input_path, 'rb') as f_in:
                content = f_in.read()
            with open(output_path, 'wb') as f_out:
                f_out.write(content)
            output_size = os.path.getsize(output_path)
            print(f"✓ Audio yozildi: {output_size} bytes (alternativ usul)")
            return output_path
        except Exception as e2:
            error_msg = f"❌ Audio yozish xatosi: {str(e2)}"
            print(error_msg)
            return None

@app.route('/api/download-audio')
def download_audio():
    """Download the generated audio"""
    try:
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_audio.mp3')
        
        if not os.path.exists(output_path):
            return flask.jsonify({'error': 'No audio file to download. Process an audio first.'}), 404
        
        # Check if file has content
        if os.path.getsize(output_path) == 0:
            return flask.jsonify({'error': 'Audio file is empty'}), 400
        
        return flask.send_file(
            output_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='tarjimon_output.mp3'
        )
    
    except Exception as e:
        print(f"Download error: {str(e)}")
        return flask.jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return flask.jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return flask.jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║                  🎤 Tarjimon - DEMO VERSION                     ║
    ║          Arab Tilidagi Audioni Ingliz Tiliga Dubbl Qilish       ║
    ╚════════════════════════════════════════════════════════════════╝
    
    ✅ Demo Server ishga tushdi!
    📍 Brauzer: http://localhost:5000
    
    🎯 Demo xususiyatlari:
       ✓ Demo ma'lumotlar bilan ishga tushdi
       ✓ Audio upload qabul qiladi
       ✓ Tarjima natijasi ko'rsatadi
       ✓ Audio yuklab olishni qo'llo qiladi
    
    📌 Haqiqiy API-larni qo'llash uchun app.py-ni ishlatish kerak
    
    ⚡ Ctrl+C - serverdan chiqish
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
