// Tarjimon Pro - Arab to English Dubbing (Audio + Video)

document.addEventListener('DOMContentLoaded', function() {
    const uploadArea       = document.getElementById('uploadArea');
    const audioInput       = document.getElementById('audioInput');
    const fileInfo         = document.getElementById('fileInfo');
    const fileName         = document.getElementById('fileName');
    const fileSize         = document.getElementById('fileSize');
    const processBtn       = document.getElementById('processBtn');
    const progressSection  = document.getElementById('progressSection');
    const resultsSection   = document.getElementById('resultsSection');
    const errorSection     = document.getElementById('errorSection');
    const resetBtn         = document.getElementById('resetBtn');
    const errorResetBtn    = document.getElementById('errorResetBtn');
    const errorMessage     = document.getElementById('errorMessage');
    const originalText     = document.getElementById('originalText');
    const translatedText   = document.getElementById('translatedText');
    const speakerInfo      = document.getElementById('speakerInfo');
    const speakerCount     = document.getElementById('speakerCount');

    // Audio player
    const audioPlayerSection = document.getElementById('audioPlayerSection');
    const audioPlayer        = document.getElementById('audioPlayer');
    const audioSource        = document.getElementById('audioSource');

    // Video player
    const videoPlayerSection = document.getElementById('videoPlayerSection');
    const videoPlayer        = document.getElementById('videoPlayer');
    const videoSource        = document.getElementById('videoSource');

    const VIDEO_EXTS = ['mp4','mkv','avi','mov','webm','flv','wmv','m4v'];

    let selectedFile = null;

    uploadArea.addEventListener('click', () => audioInput.click());

    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) handleFileSelect(e.dataTransfer.files[0]);
    });

    audioInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) handleFileSelect(e.target.files[0]);
    });

    function handleFileSelect(file) {
        const ext = file.name.split('.').pop().toLowerCase();
        const isVideo = VIDEO_EXTS.includes(ext);
        const isAudio = file.type.startsWith('audio/') || isVideo === false;

        if (!file.type.startsWith('audio/') && !file.type.startsWith('video/') && !isVideo) {
            showError('Iltimos, audio yoki video fayl tanlang!');
            return;
        }
        if (file.size > 400 * 1024 * 1024) {
            showError('Fayl hajmi 400MB dan oshmasligi kerak!');
            return;
        }

        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
        processBtn.disabled = false;
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';
    }

    processBtn.addEventListener('click', async () => {
        if (!selectedFile) return;
        await processAudio(selectedFile);
    });

    resetBtn.addEventListener('click', resetForm);
    errorResetBtn.addEventListener('click', resetForm);

    async function processAudio(file) {
        const formData = new FormData();
        formData.append('audio', file);

        progressSection.style.display = 'block';
        resultsSection.style.display  = 'none';
        errorSection.style.display    = 'none';
        processBtn.disabled = true;

        animateProgress();

        try {
            const response = await fetch('/api/process-audio', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) throw new Error(data.error || 'Noma\'lum xato yuz berdi');

            completeProgress();

            originalText.textContent   = data.original_text;
            translatedText.textContent = data.translated_text;

            if (data.num_speakers && data.num_speakers > 0) {
                speakerCount.textContent = `${data.num_speakers} ta notiq aniqlandi`;
                speakerInfo.style.display = 'block';
            } else {
                speakerInfo.style.display = 'none';
            }

            // Video yoki audio player ko'rsatish
            if (data.is_video && data.video_url) {
                videoSource.src = data.video_url + '?t=' + Date.now();
                videoPlayer.load();
                videoPlayerSection.style.display = 'block';
                audioPlayerSection.style.display = 'none';
            } else {
                audioSource.src = data.audio_url + '?t=' + Date.now();
                audioPlayer.load();
                audioPlayerSection.style.display = 'block';
                videoPlayerSection.style.display = 'none';
            }

            setTimeout(() => {
                progressSection.style.display = 'none';
                resultsSection.style.display  = 'block';
            }, 500);

        } catch (error) {
            showError(error.message);
        } finally {
            processBtn.disabled = false;
        }
    }

    // Har bir qadam qachon boshlanadi (ms)
    const STEP_DELAYS = [500, 5000, 10000, 20000, 30000];

    // Har bir qadam uchun animatsiya davomiyligi (ms) — keyingi qadamgacha bo'lgan vaqt
    const STEP_DURATIONS = [4000, 4500, 9500, 9500, 15000];

    // activeTimers — completeProgress chaqirilganda ularni bekor qilish uchun
    let activeTimers = [];

    function animateProgress() {
        const progressBars = document.querySelectorAll('.progress-bar');
        const stepNumbers  = document.querySelectorAll('.progress-step .step-number');
        const stepPercents = document.querySelectorAll('.step-percent');

        // Reset
        activeTimers.forEach(id => clearTimeout(id));
        activeTimers = [];
        stepNumbers.forEach(s => s.classList.remove('completed'));
        stepPercents.forEach(p => { p.textContent = '0%'; p.classList.remove('completed'); });
        progressBars.forEach(b => {
            b.classList.remove('active', 'completed');
            const fill = b.querySelector('.progress-fill');
            if (fill) fill.style.width = '0%';
        });

        STEP_DELAYS.forEach((delay, i) => {
            const tid = setTimeout(() => {
                if (progressBars[i]) {
                    progressBars[i].classList.add('active');
                    // foizni 0 → 99 gacha animatsiya qilish (100 faqat complete da)
                    animatePercent(
                        stepPercents[i],
                        progressBars[i].querySelector('.progress-fill'),
                        0, 99,
                        STEP_DURATIONS[i]
                    );
                }
            }, delay);
            activeTimers.push(tid);
        });
    }

    function animatePercent(labelEl, fillEl, from, to, duration) {
        if (!labelEl && !fillEl) return;
        const start = performance.now();

        function tick(now) {
            const raw     = Math.min((now - start) / duration, 1);
            // ease-out: tez boshlanib, sekinlashadi
            const eased   = 1 - Math.pow(1 - raw, 3);
            const current = Math.round(from + (to - from) * eased);

            if (labelEl) labelEl.textContent = current + '%';
            if (fillEl)  fillEl.style.width  = current + '%';

            if (raw < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
    }

    function completeProgress() {
        // Barcha timeoutlarni bekor qil
        activeTimers.forEach(id => clearTimeout(id));
        activeTimers = [];

        const progressBars = document.querySelectorAll('.progress-bar');
        const stepNumbers  = document.querySelectorAll('.progress-step .step-number');
        const stepPercents = document.querySelectorAll('.step-percent');

        progressBars.forEach(b => {
            b.classList.remove('active');
            b.classList.add('completed');
            const fill = b.querySelector('.progress-fill');
            if (fill) fill.style.width = '100%';
        });
        stepNumbers.forEach(s => s.classList.add('completed'));
        stepPercents.forEach(p => { p.textContent = '100%'; p.classList.add('completed'); });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorSection.style.display   = 'block';
        progressSection.style.display = 'none';
        resultsSection.style.display  = 'none';
        processBtn.disabled = false;
    }

    function resetForm() {
        selectedFile = null;
        audioInput.value = '';
        fileInfo.style.display        = 'none';
        processBtn.disabled           = true;
        progressSection.style.display = 'none';
        resultsSection.style.display  = 'none';
        errorSection.style.display    = 'none';
        speakerInfo.style.display     = 'none';
        audioPlayerSection.style.display = 'block';
        videoPlayerSection.style.display = 'none';
        originalText.textContent   = '';
        translatedText.textContent = '';
        speakerCount.textContent   = '';
        audioSource.src = '';
        videoSource.src = '';

        // Progress reset
        document.querySelectorAll('.step-percent').forEach(p => { p.textContent = '0%'; p.classList.remove('completed'); });
        document.querySelectorAll('.progress-bar').forEach(b => {
            b.classList.remove('active', 'completed');
            const fill = b.querySelector('.progress-fill');
            if (fill) fill.style.width = '0%';
        });
        document.querySelectorAll('.step-number').forEach(s => s.classList.remove('completed'));
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
    }

    fetch('/api/health')
        .then(r => r.json())
        .then(d => console.log('API status:', d.message))
        .catch(() => console.warn('Backend serverga ulanib bo\'lmadi.'));
});
