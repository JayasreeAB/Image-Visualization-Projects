/**
 * Vision Hub AI - Client Application Logic
 */

document.addEventListener('DOMContentLoaded', () => {
    // --- State Variables ---
    let activeMode = 'dual';
    let cameraRunning = false;
    let cameraSource = 'browser';
    let isProcessingFrame = false;
    let mediaStream = null;
    let frameLoopId = null;

    // --- DOM Elements ---
    const webcamVideo = document.getElementById('webcamVideo');
    const outputCanvas = document.getElementById('outputCanvas');
    const ctx = outputCanvas.getContext('2d');
    const serverStreamImg = document.getElementById('serverStreamImg');
    const videoPlaceholder = document.getElementById('videoPlaceholder');
    
    const toggleCameraBtn = document.getElementById('toggleCameraBtn');
    const cameraStatusBadge = document.getElementById('cameraStatusBadge');
    const cameraStatusText = document.getElementById('cameraStatusText');
    const cameraSourceSelect = document.getElementById('cameraSourceSelect');
    const snapshotBtn = document.getElementById('snapshotBtn');
    const navTabs = document.querySelectorAll('.nav-tab');
    const activeModeDisplay = document.getElementById('activeModeDisplay');
    const brightnessDimmerOverlay = document.getElementById('brightnessDimmerOverlay');

    // Metrics DOM
    const metricFaceCount = document.getElementById('metricFaceCount');
    const metricBrightness = document.getElementById('metricBrightness');
    const metricDistance = document.getElementById('metricDistance');
    const fpsCounter = document.getElementById('fpsCounter');

    // Controls DOM
    const brightnessRange = document.getElementById('brightnessRange');
    const brightnessValText = document.getElementById('brightnessValText');
    const minNeighborsRange = document.getElementById('minNeighborsRange');
    const minNeighborsVal = document.getElementById('minNeighborsVal');
    const scaleFactorRange = document.getElementById('scaleFactorRange');
    const scaleFactorVal = document.getElementById('scaleFactorVal');

    // Offscreen Canvas for Frame Extraction
    const offscreenCanvas = document.createElement('canvas');
    const offscreenCtx = offscreenCanvas.getContext('2d');

    // --- Tab Mode Switching ---
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            navTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            activeMode = tab.getAttribute('data-mode');

            const modeLabels = {
                'dual': 'Dual Mode (Faces + Hand Brightness)',
                'face': 'Face Counter & Eye Tracking Mode',
                'hand': 'Hand Gesture Brightness Control Mode'
            };
            activeModeDisplay.textContent = modeLabels[activeMode] || activeMode;
        });
    });

    // --- Camera Toggle Handler ---
    toggleCameraBtn.addEventListener('click', () => {
        if (!cameraRunning) {
            startCamera();
        } else {
            stopCamera();
        }
    });

    // --- Camera Source Selector ---
    cameraSourceSelect.addEventListener('change', (e) => {
        cameraSource = e.target.value;
        if (cameraRunning) {
            stopCamera();
            startCamera();
        }
    });

    // --- Start Camera Stream ---
    async function startCamera() {
        if (cameraSource === 'browser') {
            try {
                mediaStream = await navigator.mediaDevices.getUserMedia({
                    video: { width: { ideal: 1280 }, height: { ideal: 720 } }
                });
                webcamVideo.srcObject = mediaStream;
                await webcamVideo.play();

                // Set canvas dimensions
                outputCanvas.width = webcamVideo.videoWidth || 640;
                outputCanvas.height = webcamVideo.videoHeight || 480;
                offscreenCanvas.width = outputCanvas.width;
                offscreenCanvas.height = outputCanvas.height;

                serverStreamImg.style.display = 'none';
                outputCanvas.style.display = 'block';
                videoPlaceholder.style.display = 'none';

                cameraRunning = true;
                updateCameraStatusUI(true, 'Browser Webcam Active');
                
                // Start processing loop
                requestAnimationFrame(processFrameLoop);

            } catch (err) {
                console.error("Camera access error:", err);
                alert("Could not access camera. Please allow camera permissions in your browser.");
                updateCameraStatusUI(false, 'Camera Error');
            }
        } else if (cameraSource === 'server') {
            serverStreamImg.src = '/api/video_feed';
            serverStreamImg.style.display = 'block';
            outputCanvas.style.display = 'none';
            videoPlaceholder.style.display = 'none';

            cameraRunning = true;
            updateCameraStatusUI(true, 'Server Camera Active');
        }
    }

    // --- Stop Camera Stream ---
    function stopCamera() {
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            mediaStream = null;
        }
        if (frameLoopId) {
            cancelAnimationFrame(frameLoopId);
            frameLoopId = null;
        }
        serverStreamImg.src = '';
        serverStreamImg.style.display = 'none';
        outputCanvas.style.display = 'none';
        videoPlaceholder.style.display = 'flex';

        cameraRunning = false;
        updateCameraStatusUI(false, 'Camera Off');
    }

    // --- UI Status Updater ---
    function updateCameraStatusUI(active, text) {
        if (active) {
            cameraStatusBadge.querySelector('.status-dot').className = 'status-dot online';
            cameraStatusText.textContent = text;
            toggleCameraBtn.innerHTML = '<i class="fa-solid fa-video-slash"></i> Stop Camera';
            toggleCameraBtn.className = 'btn btn-secondary';
        } else {
            cameraStatusBadge.querySelector('.status-dot').className = 'status-dot offline';
            cameraStatusText.textContent = text;
            toggleCameraBtn.innerHTML = '<i class="fa-solid fa-video"></i> Start Camera';
            toggleCameraBtn.className = 'btn btn-primary';
        }
    }

    // --- Frame Extraction & API Processing Loop ---
    async function processFrameLoop() {
        if (!cameraRunning || cameraSource !== 'browser') return;

        if (!isProcessingFrame && webcamVideo.readyState === webcamVideo.HAVE_ENOUGH_DATA) {
            isProcessingFrame = true;

            // Draw current video frame to offscreen canvas
            offscreenCtx.drawImage(webcamVideo, 0, 0, offscreenCanvas.width, offscreenCanvas.height);
            const base64Image = offscreenCanvas.toDataURL('image/jpeg', 0.75);

            try {
                const scaleVal = (parseInt(scaleFactorRange.value) / 100).toFixed(2);
                
                const response = await fetch('/api/process_frame', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        image: base64Image,
                        mode: activeMode,
                        min_neighbors: parseInt(minNeighborsRange.value),
                        scale_factor: parseFloat(scaleVal)
                    })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    // Render annotated frame onto output canvas
                    const img = new Image();
                    img.onload = () => {
                        ctx.drawImage(img, 0, 0, outputCanvas.width, outputCanvas.height);
                    };
                    img.src = data.image;

                    // Update Metrics Dashboard
                    metricFaceCount.textContent = data.face_count;
                    metricBrightness.textContent = `${data.brightness}%`;
                    metricDistance.innerHTML = `${data.distance} <small>px</small>`;
                    fpsCounter.textContent = data.fps;

                    // Sync Web Brightness Dimmer Overlay
                    applyBrightnessOverlay(data.brightness);
                    brightnessRange.value = data.brightness;
                    brightnessValText.textContent = `${data.brightness}%`;
                }
            } catch (err) {
                console.error("Frame processing API error:", err);
            } finally {
                isProcessingFrame = false;
            }
        }

        frameLoopId = requestAnimationFrame(processFrameLoop);
    }

    // --- Apply Page Brightness Overlay ---
    function applyBrightnessOverlay(brightnessPercent) {
        // Brightness 100% -> opacity 0 (no dimming)
        // Brightness 0% -> opacity 0.85 (darkened)
        const dimOpacity = (1 - (brightnessPercent / 100)) * 0.85;
        brightnessDimmerOverlay.style.opacity = Math.max(0, Math.min(0.85, dimOpacity));
    }

    // --- Manual Brightness Slider Event ---
    brightnessRange.addEventListener('input', async (e) => {
        const val = parseInt(e.target.value);
        brightnessValText.textContent = `${val}%`;
        metricBrightness.textContent = `${val}%`;
        applyBrightnessOverlay(val);

        try {
            await fetch('/api/set_brightness', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ brightness: val })
            });
        } catch (err) {
            console.error("Set brightness error:", err);
        }
    });

    // --- Slider UI Display Updaters ---
    minNeighborsRange.addEventListener('input', (e) => {
        minNeighborsVal.textContent = e.target.value;
    });

    scaleFactorRange.addEventListener('input', (e) => {
        scaleFactorVal.textContent = (parseInt(e.target.value) / 100).toFixed(2);
    });

    // --- Snapshot Download Handler ---
    snapshotBtn.addEventListener('click', () => {
        if (!cameraRunning) {
            alert("Please start the camera to capture a snapshot.");
            return;
        }

        const link = document.createElement('a');
        link.download = `vision-hub-snapshot-${Date.now()}.jpg`;
        if (cameraSource === 'browser') {
            link.href = outputCanvas.toDataURL('image/jpeg');
        } else {
            link.href = serverStreamImg.src;
        }
        link.click();
    });
});
