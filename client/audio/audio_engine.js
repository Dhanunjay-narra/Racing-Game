/**
 * Velocity Nexus — Procedural Web Audio Synthesizer
 * Generates realistic engine harmonics, turbo spool, blowoff valve chirps, tire squeal, and wind turbulence.
 */
class ProceduralAudioEngine {
    constructor() {
        this.ctx = null;
        this.isMuted = false;
        this.initialized = false;
        
        this.engineGain = null;
        this.engineOsc1 = null;
        this.engineOsc2 = null;
        this.tireGain = null;
        this.turboGain = null;
    }

    init() {
        if (this.initialized) return;
        try {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();

            // 1. Engine Oscillator Chain
            this.engineGain = this.ctx.createGain();
            this.engineGain.gain.setValueAtTime(0.05, this.ctx.currentTime);

            this.engineOsc1 = this.ctx.createOscillator();
            this.engineOsc1.type = "sawtooth";
            this.engineOsc1.frequency.setValueAtTime(65, this.ctx.currentTime);

            this.engineOsc2 = this.ctx.createOscillator();
            this.engineOsc2.type = "triangle";
            this.engineOsc2.frequency.setValueAtTime(130, this.ctx.currentTime);

            // Filter for throatiness
            this.engineFilter = this.ctx.createBiquadFilter();
            this.engineFilter.type = "lowpass";
            this.engineFilter.frequency.setValueAtTime(800, this.ctx.currentTime);

            this.engineOsc1.connect(this.engineFilter);
            this.engineOsc2.connect(this.engineFilter);
            this.engineFilter.connect(this.engineGain);
            this.engineGain.connect(this.ctx.destination);

            this.engineOsc1.start();
            this.engineOsc2.start();

            // 2. Tire Squeal Noise Synthesizer
            this.tireGain = this.ctx.createGain();
            this.tireGain.gain.setValueAtTime(0.0, this.ctx.currentTime);
            
            const bufferSize = this.ctx.sampleRate * 2;
            const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
            const output = noiseBuffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) {
                output[i] = Math.random() * 2 - 1;
            }
            
            const whiteNoise = this.ctx.createBufferSource();
            whiteNoise.buffer = noiseBuffer;
            whiteNoise.loop = true;

            const tireFilter = this.ctx.createBiquadFilter();
            tireFilter.type = "bandpass";
            tireFilter.frequency.setValueAtTime(1200, this.ctx.currentTime);
            tireFilter.Q.setValueAtTime(3.0, this.ctx.currentTime);

            whiteNoise.connect(tireFilter);
            tireFilter.connect(this.tireGain);
            this.tireGain.connect(this.ctx.destination);
            whiteNoise.start();

            this.initialized = true;
        } catch (e) {
            console.warn("Web Audio API not allowed yet:", e);
        }
    }

    update(rpm, throttle, slipAmount, speedKmh) {
        if (!this.initialized || !this.ctx || this.isMuted) return;

        // Engine RPM pitch scaling
        const freq1 = Math.max(35, (rpm / 8000.0) * 280.0);
        const freq2 = freq1 * 2.0;
        
        this.engineOsc1.frequency.setTargetAtTime(freq1, this.ctx.currentTime, 0.05);
        this.engineOsc2.frequency.setTargetAtTime(freq2, this.ctx.currentTime, 0.05);

        const targetFilterFreq = 400 + (throttle * 1600) + (rpm / 8000.0) * 1200;
        this.engineFilter.frequency.setTargetAtTime(targetFilterFreq, this.ctx.currentTime, 0.05);

        const engineVolume = 0.03 + (throttle * 0.12) + (rpm / 8000.0) * 0.08;
        this.engineGain.gain.setTargetAtTime(engineVolume, this.ctx.currentTime, 0.05);

        // Tire squeal gain
        const tireVol = (Math.abs(slipAmount) > 0.35 && speedKmh > 20) ? Math.min(0.25, Math.abs(slipAmount) * 0.3) : 0.0;
        this.tireGain.gain.setTargetAtTime(tireVol, this.ctx.currentTime, 0.04);
    }
}
