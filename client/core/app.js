/**
 * Velocity Nexus — Client Application Entry Point & Race Orchestrator
 */
class VelocityNexusApp {
    constructor() {
        this.token = null;
        this.user = {
            id: "guest",
            username: "ApexLegend",
            displayName: "Apex Legend",
            level: 1,
            credits: 50000,
            gold: 500
        };

        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.playerCar = null;
        this.cameraController = null;
        this.audio = new ProceduralAudioEngine();
        
        this.isRacing = false;
        this.speedKmh = 0;
        this.rpm = 900;
        this.currentGear = 1;
        this.nitroAmount = 100.0;
        this.lap = 1;
        this.lapStartTime = 0;
        
        this.keys = {};
        this.selectedCarId = "apex_rs1";
    }

    init() {
        this.setupThreeJS();
        this.setupEventListeners();
        this.buildTrack();
        this.spawnPlayerCar();
        this.animate();
        lucide.createIcons();
    }

    setupThreeJS() {
        const container = document.getElementById("canvas-container");
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x050515);
        this.scene.fog = new THREE.FogExp2(0x050515, 0.005);

        this.camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        container.appendChild(this.renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404060, 1.2);
        this.scene.add(ambientLight);

        const dirLight = new THREE.DirectionalLight(0x00ffff, 2.0);
        dirLight.position.set(50, 100, 50);
        dirLight.castShadow = true;
        dirLight.shadow.mapSize.width = 2048;
        dirLight.shadow.mapSize.height = 2048;
        this.scene.add(dirLight);

        window.addEventListener("resize", () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    buildTrack() {
        // Procedural circuit road
        const trackRadiusX = 90;
        const trackRadiusZ = 60;
        const trackGeo = new THREE.RingGeometry(50, 68, 64);
        trackGeo.rotateX(-Math.PI / 2);
        const trackMat = new THREE.MeshStandardMaterial({ color: 0x1a1a24, roughness: 0.4 });
        const road = new THREE.Mesh(trackGeo, trackMat);
        road.receiveShadow = true;
        this.scene.add(road);

        // Ground plane
        const groundGeo = new THREE.PlaneGeometry(1000, 1000);
        groundGeo.rotateX(-Math.PI / 2);
        const groundMat = new THREE.MeshStandardMaterial({ color: 0x080914, roughness: 0.9 });
        const ground = new THREE.Mesh(groundGeo, groundMat);
        ground.position.y = -0.05;
        this.scene.add(ground);

        // Neon trackside barriers
        const barrierMat = new THREE.MeshBasicMaterial({ color: 0x00d2ff });
        for (let i = 0; i < 32; i++) {
            const angle = (i / 32) * Math.PI * 2;
            const bGeo = new THREE.BoxGeometry(1, 1.2, 8);
            const barrier = new THREE.Mesh(bGeo, barrierMat);
            barrier.position.set(Math.cos(angle) * 70, 0.6, Math.sin(angle) * 70);
            barrier.rotation.y = -angle;
            this.scene.add(barrier);
        }
    }

    spawnPlayerCar() {
        this.playerCar = VehicleMeshGenerator.createCarMesh({
            paintColor: 0x00d2ff,
            rimColor: 0x111111,
            spoilerType: "gt",
            underglowColor: 0x00ffff
        });
        this.playerCar.position.set(0, 0, 59);
        this.playerCar.rotation.y = Math.PI / 2;
        this.scene.add(this.playerCar);

        this.cameraController = new DynamicCameraController(this.camera, this.playerCar);
    }

    setupEventListeners() {
        window.addEventListener("keydown", (e) => {
            this.keys[e.key.toLowerCase()] = true;
            this.audio.init();
            if (e.key.toLowerCase() === "c") {
                const modes = ["CHASE", "COCKPIT", "HOOD", "ORBIT"];
                const nextIdx = (modes.indexOf(this.cameraController.mode) + 1) % modes.length;
                this.cameraController.setMode(modes[nextIdx]);
            }
        });

        window.addEventListener("keyup", (e) => {
            this.keys[e.key.toLowerCase()] = false;
        });
    }

    async quickLogin() {
        this.audio.init();
        try {
            const username = document.getElementById("loginUsername").value;
            const password = document.getElementById("loginPassword").value;

            // Try register / login with API
            const res = await fetch("/api/v1/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username_or_email: username, password: password })
            });

            if (res.ok) {
                const data = await res.json();
                this.token = data.access_token;
                this.user.displayName = data.display_name;
                this.user.credits = data.credits;
                this.user.gold = data.nexus_gold;
                this.user.level = data.level;
            }
        } catch (e) {
            console.log("Local mock session enabled");
        }

        document.getElementById("userDisplayName").textContent = this.user.displayName;
        document.getElementById("walletCredits").textContent = this.user.credits.toLocaleString();
        document.getElementById("walletGold").textContent = this.user.gold.toLocaleString();
        document.getElementById("authSection").classList.add("hidden");
    }

    startRace() {
        this.audio.init();
        this.isRacing = true;
        this.lap = 1;
        this.lapStartTime = Date.now();
        document.getElementById("mainMenuScreen").classList.add("hidden");
        document.getElementById("raceHudScreen").classList.remove("hidden");
        this.cameraController.setMode("CHASE");
    }

    openGarage() {
        document.getElementById("garageModal").classList.remove("hidden");
        this.cameraController.setMode("ORBIT");
    }

    closeGarage() {
        document.getElementById("garageModal").classList.add("hidden");
        this.cameraController.setMode("CHASE");
    }

    openCareer() {
        alert("Career Mode: 6 Chapters Unlocked! Starting Chapter 1: Rookie Ignition.");
    }

    openDriverDNA() {
        document.getElementById("dnaModal").classList.remove("hidden");
        const container = document.getElementById("dnaBarsContainer");
        const stats = [
            { name: "Aggression", val: 84 },
            { name: "Cornering Precision", val: 92 },
            { name: "Overtaking", val: 78 },
            { name: "Drifting Control", val: 95 },
            { name: "Consistency", val: 70 },
            { name: "Wet Racing", val: 65 },
            { name: "Risk Management", val: 80 }
        ];
        container.innerHTML = stats.map(s => `
            <div>
                <div class="flex justify-between text-slate-300"><span>${s.name}</span><span class="text-amber-400 font-bold">${s.val}%</span></div>
                <div class="w-full h-2 bg-slate-800 rounded-full overflow-hidden mt-1">
                    <div class="h-full bg-amber-400" style="width:${s.val}%"></div>
                </div>
            </div>
        `).join("");
    }

    closeDriverDNA() {
        document.getElementById("dnaModal").classList.add("hidden");
    }

    openAdmin() {
        window.open("/docs", "_blank");
    }

    setPaint(hex) {
        if (this.playerCar) {
            this.playerCar.updatePaintColor(hex);
        }
    }

    changeLanguage(lang) {
        const translations = {
            en: { start: "Start 3D Race" },
            te: { start: "రేస్ ప్రారంభించు" },
            hi: { start: "दौड़ शुरू करें" },
            ta: { start: "பந்தயத்தைத் தொடங்கு" }
        };
        const text = translations[lang] || translations.en;
        document.getElementById("btnStartRace").textContent = text.start;
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const dt = 0.016;
        let throttle = 0;
        let steer = 0;
        let brake = 0;
        let nitro = false;

        if (this.isRacing) {
            if (this.keys["w"] || this.keys["arrowup"]) throttle = 1.0;
            if (this.keys["s"] || this.keys["arrowdown"]) brake = 1.0;
            if (this.keys["a"] || this.keys["arrowleft"]) steer = 1.0;
            if (this.keys["d"] || this.keys["arrowright"]) steer = -1.0;
            if (this.keys["shift"] && this.nitroAmount > 0) {
                nitro = true;
                this.nitroAmount = Math.max(0, this.nitroAmount - dt * 25);
            } else if (!this.keys["shift"]) {
                this.nitroAmount = Math.min(100, this.nitroAmount + dt * 10);
            }

            // Simple physics integration for immediate response
            const maxSpeed = nitro ? 340 : 275;
            if (throttle > 0) {
                this.speedKmh = Math.min(maxSpeed, this.speedKmh + (nitro ? 95 : 65) * dt);
            } else if (brake > 0) {
                this.speedKmh = Math.max(0, this.speedKmh - 140 * dt);
            } else {
                this.speedKmh = Math.max(0, this.speedKmh - 15 * dt);
            }

            if (this.speedKmh > 0) {
                this.playerCar.rotation.y += steer * (this.speedKmh / maxSpeed) * 2.2 * dt;
                const speedMps = this.speedKmh / 3.6;
                this.playerCar.position.x += Math.sin(this.playerCar.rotation.y) * speedMps * dt;
                this.playerCar.position.z += Math.cos(this.playerCar.rotation.y) * speedMps * dt;
            }

            // RPM and Gear simulation
            this.rpm = 900 + (this.speedKmh % 60) * 120;
            this.currentGear = Math.min(6, Math.floor(this.speedKmh / 50) + 1);

            // Audio & HUD update
            this.audio.update(this.rpm, throttle, steer * 0.4, this.speedKmh);
            
            document.getElementById("hudSpeed").textContent = Math.floor(this.speedKmh);
            document.getElementById("hudGear").textContent = this.speedKmh === 0 ? "N" : this.currentGear;
            document.getElementById("hudRpm").textContent = `${Math.floor(this.rpm)} RPM`;
            document.getElementById("hudNitroBar").style.width = `${this.nitroAmount}%`;

            const elapsed = Date.now() - this.lapStartTime;
            const mins = String(Math.floor(elapsed / 60000)).padStart(2, '0');
            const secs = String(Math.floor((elapsed % 60000) / 1000)).padStart(2, '0');
            const ms = String(elapsed % 1000).padStart(3, '0');
            document.getElementById("hudLapTime").textContent = `${mins}:${secs}.${ms}`;
        }

        if (this.cameraController) {
            this.cameraController.update(dt, this.speedKmh, steer, nitro);
        }

        this.renderer.render(this.scene, this.camera);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    window.app = new VelocityNexusApp();
    window.app.init();
});
