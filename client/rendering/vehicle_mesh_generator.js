/**
 * Velocity Nexus — Procedural 3D Vehicle Geometry Generator
 * Generates detailed multi-part vehicle meshes with customizable paint, rims, spoiler, and underglow.
 */
class VehicleMeshGenerator {
    static createCarMesh(spec = {}) {
        const group = new THREE.Group();
        const paintColor = spec.paintColor || 0x00d2ff;
        const rimColor = spec.rimColor || 0x111111;
        const spoilerType = spec.spoilerType || "sport";
        const underglowColor = spec.underglowColor || null;

        // 1. Chassis Main Body
        const bodyMat = new THREE.MeshStandardMaterial({
            color: paintColor,
            roughness: 0.15,
            metalness: 0.85,
            clearcoat: 1.0,
            clearcoatRoughness: 0.1
        });
        
        const bodyGeo = new THREE.BoxGeometry(1.9, 0.55, 4.4);
        const bodyMesh = new THREE.Mesh(bodyGeo, bodyMat);
        bodyMesh.position.y = 0.55;
        bodyMesh.castShadow = true;
        bodyMesh.receiveShadow = true;
        group.add(bodyMesh);

        // 2. Cabin / Greenhouse
        const glassMat = new THREE.MeshPhysicalMaterial({
            color: 0x0a0a15,
            roughness: 0.05,
            metalness: 0.9,
            transmission: 0.6,
            transparent: true,
            opacity: 0.85
        });
        const cabinGeo = new THREE.BoxGeometry(1.6, 0.48, 2.2);
        const cabinMesh = new THREE.Mesh(cabinGeo, glassMat);
        cabinMesh.position.set(0, 0.95, -0.2);
        cabinMesh.castShadow = true;
        group.add(cabinMesh);

        // 3. Hood Aerodynamic Slope
        const hoodGeo = new THREE.BoxGeometry(1.7, 0.25, 1.4);
        const hoodMesh = new THREE.Mesh(hoodGeo, bodyMat);
        hoodMesh.position.set(0, 0.62, 1.4);
        hoodMesh.rotation.x = 0.15;
        group.add(hoodMesh);

        // 4. Wheels & Brake Calipers
        const wheelMat = new THREE.MeshStandardMaterial({ color: 0x1a1a1a, roughness: 0.8 });
        const rimMat = new THREE.MeshStandardMaterial({ color: rimColor, metalness: 0.9, roughness: 0.2 });
        const caliperMat = new THREE.MeshStandardMaterial({ color: 0xff0044, roughness: 0.3 });

        const wheelGeo = new THREE.CylinderGeometry(0.38, 0.38, 0.32, 24);
        wheelGeo.rotateZ(Math.PI / 2);

        const wheelPositions = [
            [-0.95, 0.38, 1.35],  // Front Left
            [0.95, 0.38, 1.35],   // Front Right
            [-0.95, 0.38, -1.35], // Rear Left
            [0.95, 0.38, -1.35]   // Rear Right
        ];

        group.wheels = [];
        wheelPositions.forEach((pos, idx) => {
            const wheelHolder = new THREE.Group();
            wheelHolder.position.set(...pos);

            const tire = new THREE.Mesh(wheelGeo, wheelMat);
            tire.castShadow = true;
            wheelHolder.add(tire);

            const rimGeo = new THREE.CylinderGeometry(0.24, 0.24, 0.33, 16);
            rimGeo.rotateZ(Math.PI / 2);
            const rim = new THREE.Mesh(rimGeo, rimMat);
            wheelHolder.add(rim);

            group.add(wheelHolder);
            group.wheels.push(wheelHolder);
        });

        // 5. Headlights & Taillights
        const headlightMat = new THREE.MeshBasicMaterial({ color: 0x88ffff });
        const headlightGeo = new THREE.BoxGeometry(0.35, 0.1, 0.1);
        
        const hlLeft = new THREE.Mesh(headlightGeo, headlightMat);
        hlLeft.position.set(-0.65, 0.62, 2.18);
        group.add(hlLeft);

        const hlRight = new THREE.Mesh(headlightGeo, headlightMat);
        hlRight.position.set(0.65, 0.62, 2.18);
        group.add(hlRight);

        const taillightMat = new THREE.MeshBasicMaterial({ color: 0xff0022 });
        const taillightGeo = new THREE.BoxGeometry(1.6, 0.08, 0.1);
        const taillight = new THREE.Mesh(taillightGeo, taillightMat);
        taillight.position.set(0, 0.65, -2.18);
        group.add(taillight);

        // 6. GT Spoiler
        if (spoilerType !== "none") {
            const spoilerMat = new THREE.MeshStandardMaterial({ color: 0x111111, metalness: 0.7, roughness: 0.3 });
            const wingGeo = new THREE.BoxGeometry(1.8, 0.06, 0.4);
            const wing = new THREE.Mesh(wingGeo, spoilerMat);
            wing.position.set(0, 1.15, -2.0);
            wing.castShadow = true;
            group.add(wing);

            const strutGeo = new THREE.BoxGeometry(0.06, 0.35, 0.1);
            const sLeft = new THREE.Mesh(strutGeo, spoilerMat);
            sLeft.position.set(-0.55, 0.95, -1.95);
            group.add(sLeft);

            const sRight = new THREE.Mesh(strutGeo, spoilerMat);
            sRight.position.set(0.55, 0.95, -1.95);
            group.add(sRight);
        }

        // 7. Underglow Neon Light
        if (underglowColor) {
            const underLight = new THREE.PointLight(underglowColor, 3.5, 3.5);
            underLight.position.set(0, 0.1, 0);
            group.add(underLight);
        }

        group.updatePaintColor = (hex) => {
            bodyMat.color.setHex(hex);
            hoodMesh.material.color.setHex(hex);
        };

        return group;
    }
}
