/**
 * Velocity Nexus — Dynamic Multi-Mode Camera Controller
 * Supports Chase, Cockpit, Hood, Orbit Showroom, and Cinematic angles with speed FOV scaling.
 */
class DynamicCameraController {
    constructor(camera, targetMesh) {
        this.camera = camera;
        this.target = targetMesh;
        this.mode = "CHASE"; // CHASE, COCKPIT, HOOD, ORBIT
        
        this.baseFov = 65;
        this.currentFov = 65;
        this.orbitAngle = 0;
    }

    setMode(mode) {
        this.mode = mode;
    }

    update(dt, speedKmh, steeringInput, isNitroActive) {
        if (!this.target) return;

        const targetPos = this.target.position;
        const targetRotY = this.target.rotation.y;

        // Dynamic FOV scaling based on speed & nitro
        const fovBonus = (speedKmh / 350.0) * 22.0 + (isNitroActive ? 12.0 : 0.0);
        this.currentFov += (this.baseFov + fovBonus - this.currentFov) * dt * 4.0;
        this.camera.fov = this.currentFov;
        this.camera.updateProjectionMatrix();

        if (this.mode === "CHASE") {
            // Smooth Chase Camera behind vehicle
            const distBehind = 6.2 + (speedKmh / 400.0) * 2.0;
            const heightAbove = 2.4;

            const desiredX = targetPos.x - Math.sin(targetRotY) * distBehind - steeringInput * 0.4;
            const desiredZ = targetPos.z - Math.cos(targetRotY) * distBehind;
            const desiredY = targetPos.y + heightAbove;

            this.camera.position.x += (desiredX - this.camera.position.x) * dt * 8.0;
            this.camera.position.y += (desiredY - this.camera.position.y) * dt * 6.0;
            this.camera.position.z += (desiredZ - this.camera.position.z) * dt * 8.0;

            const lookTarget = new THREE.Vector3(
                targetPos.x + Math.sin(targetRotY) * 8.0,
                targetPos.y + 0.9,
                targetPos.z + Math.cos(targetRotY) * 8.0
            );
            this.camera.lookAt(lookTarget);

        } else if (this.mode === "COCKPIT") {
            this.camera.position.set(
                targetPos.x - Math.sin(targetRotY) * 0.2 - 0.35,
                targetPos.y + 0.95,
                targetPos.z - Math.cos(targetRotY) * 0.2
            );
            const lookTarget = new THREE.Vector3(
                targetPos.x + Math.sin(targetRotY) * 20.0,
                targetPos.y + 0.85,
                targetPos.z + Math.cos(targetRotY) * 20.0
            );
            this.camera.lookAt(lookTarget);

        } else if (this.mode === "HOOD") {
            this.camera.position.set(
                targetPos.x + Math.sin(targetRotY) * 1.2,
                targetPos.y + 0.75,
                targetPos.z + Math.cos(targetRotY) * 1.2
            );
            const lookTarget = new THREE.Vector3(
                targetPos.x + Math.sin(targetRotY) * 25.0,
                targetPos.y + 0.7,
                targetPos.z + Math.cos(targetRotY) * 25.0
            );
            this.camera.lookAt(lookTarget);

        } else if (this.mode === "ORBIT") {
            this.orbitAngle += dt * 0.45;
            const radius = 5.5;
            this.camera.position.set(
                targetPos.x + Math.sin(this.orbitAngle) * radius,
                targetPos.y + 1.8,
                targetPos.z + Math.cos(this.orbitAngle) * radius
            );
            this.camera.lookAt(new THREE.Vector3(targetPos.x, targetPos.y + 0.5, targetPos.z));
        }
    }
}
