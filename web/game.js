// 3D Battle Game with Three.js

class GameEngine {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas'), antialias: true, alpha: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.setClearColor(0x1a1a2e, 1);

        this.camera.position.set(0, 5, 15);
        this.camera.lookAt(0, 0, 0);

        // Game State
        this.player = { hp: 100, maxHp: 100, level: 5, power: 125 };
        this.enemy = { hp: 100, maxHp: 100, level: 8, power: 250 };
        this.gameState = 'battle'; // 'battle', 'victory', 'defeat'
        this.roundTime = 5;
        this.roundTimeLeft = 5;
        this.isPlayerTurn = true;
        this.tapCount = 0;
        this.comboMultiplier = 1;
        this.battleLog = [];

        // 3D Objects
        this.playerModel = null;
        this.enemyModel = null;
        this.particleSystem = [];

        this.initScene();
        this.addLighting();
        this.createModels();
        this.setupEventListeners();
        this.animate();
    }

    initScene() {
        // Background/Sky
        const skyGeometry = new THREE.SphereGeometry(100, 32, 32);
        const skyMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a4d7a,
            side: THREE.BackSide
        });
        const skyMesh = new THREE.Mesh(skyGeometry, skyMaterial);
        this.scene.add(skyMesh);

        // Ground
        const groundGeometry = new THREE.PlaneGeometry(50, 50);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x8b7355,
            roughness: 0.8
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    addLighting() {
        // Ambient Light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        // Directional Light (Sun)
        const sunLight = new THREE.DirectionalLight(0xffaa44, 0.8);
        sunLight.position.set(10, 20, 10);
        sunLight.castShadow = true;
        sunLight.shadow.camera.left = -50;
        sunLight.shadow.camera.right = 50;
        sunLight.shadow.camera.top = 50;
        sunLight.shadow.camera.bottom = -50;
        this.scene.add(sunLight);

        // Point Light (Arena)
        const pointLight = new THREE.PointLight(0x00ffff, 0.5);
        pointLight.position.set(0, 10, 0);
        this.scene.add(pointLight);
    }

    createModels() {
        // Create Player (Pepka)
        this.playerModel = this.createCharacter(0xffaa00, 'left');
        this.playerModel.position.x = -5;
        this.playerModel.position.z = 0;
        this.scene.add(this.playerModel);

        // Create Enemy (Dragon)
        this.enemyModel = this.createDragon();
        this.enemyModel.position.x = 5;
        this.enemyModel.position.z = 0;
        this.scene.add(this.enemyModel);
    }

    createCharacter(color, side) {
        const group = new THREE.Group();

        // Body
        const bodyGeometry = new THREE.CapsuleGeometry(0.5, 2, 4, 8);
        const bodyMaterial = new THREE.MeshStandardMaterial({ color });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.castShadow = true;
        group.add(body);

        // Head
        const headGeometry = new THREE.SphereGeometry(0.6, 32, 32);
        const headMaterial = new THREE.MeshStandardMaterial({ color });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        head.position.y = 1.5;
        head.castShadow = true;
        group.add(head);

        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.15, 16, 16);
        const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x000000 });
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.2, 2, 0.5);
        leftEye.castShadow = true;
        group.add(leftEye);
        
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.2, 2, 0.5);
        rightEye.castShadow = true;
        group.add(rightEye);

        // Arms
        const armGeometry = new THREE.CapsuleGeometry(0.2, 1.5, 4, 8);
        const armMaterial = new THREE.MeshStandardMaterial({ color });
        
        const leftArm = new THREE.Mesh(armGeometry, armMaterial);
        leftArm.position.set(-0.8, 0.5, 0);
        leftArm.castShadow = true;
        group.add(leftArm);
        
        const rightArm = new THREE.Mesh(armGeometry, armMaterial);
        rightArm.position.set(0.8, 0.5, 0);
        rightArm.castShadow = true;
        group.add(rightArm);

        // Store for animation
        group.userData.leftArm = leftArm;
        group.userData.rightArm = rightArm;
        group.userData.head = head;
        group.userData.side = side;

        return group;
    }

    createDragon() {
        const group = new THREE.Group();

        // Body
        const bodyGeometry = new THREE.CapsuleGeometry(1, 3, 4, 8);
        const bodyMaterial = new THREE.MeshStandardMaterial({ color: 0xff4444 });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.castShadow = true;
        group.add(body);

        // Head
        const headGeometry = new THREE.SphereGeometry(1, 32, 32);
        const headMaterial = new THREE.MeshStandardMaterial({ color: 0xcc0000 });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        head.position.y = 2;
        head.castShadow = true;
        group.add(head);

        // Eyes
        const eyeGeometry = new THREE.SphereGeometry(0.3, 16, 16);
        const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0xffff00 });
        const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        leftEye.position.set(-0.4, 2.5, 0.8);
        leftEye.castShadow = true;
        group.add(leftEye);
        
        const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
        rightEye.position.set(0.4, 2.5, 0.8);
        rightEye.castShadow = true;
        group.add(rightEye);

        // Wings
        const wingGeometry = new THREE.BoxGeometry(0.5, 2, 3);
        const wingMaterial = new THREE.MeshStandardMaterial({ color: 0xaa0000 });
        
        const leftWing = new THREE.Mesh(wingGeometry, wingMaterial);
        leftWing.position.set(-1.2, 1, 0);
        leftWing.castShadow = true;
        group.add(leftWing);
        
        const rightWing = new THREE.Mesh(wingGeometry, wingMaterial);
        rightWing.position.set(1.2, 1, 0);
        rightWing.castShadow = true;
        group.add(rightWing);

        group.userData.leftWing = leftWing;
        group.userData.rightWing = rightWing;
        group.userData.head = head;
        group.userData.leftEye = leftEye;
        group.userData.rightEye = rightEye;

        return group;
    }

    setupEventListeners() {
        document.getElementById('tap-btn').addEventListener('click', () => this.onTap());
        window.addEventListener('resize', () => this.onWindowResize());
    }

    onTap() {
        if (this.gameState !== 'battle' || !this.isPlayerTurn) return;

        this.tapCount++;
        const baseDamage = 15 + Math.random() * 10;
        const damage = Math.floor(baseDamage * this.comboMultiplier);
        
        this.enemy.hp = Math.max(0, this.enemy.hp - damage);
        
        // Animation
        this.playAttackAnimation(this.playerModel, 'player');
        this.createDamageNumber(this.enemyModel.position, damage);
        this.createParticles(this.enemyModel.position, 0xff4444);
        this.playSound('attack');

        // Combo
        this.comboMultiplier = Math.min(3, 1 + this.tapCount * 0.1);
        
        // Log
        this.addBattleLog(`You dealt ${damage} damage!`);

        // Update UI
        this.updateHPBars();

        // Check victory
        if (this.enemy.hp <= 0) {
            this.endBattle('victory');
        }
    }

    playAttackAnimation(model, type) {
        if (type === 'player') {
            const arm = model.userData.rightArm;
            const originalRotation = arm.rotation.z;
            
            // Swing animation
            let swing = 0;
            const swingInterval = setInterval(() => {
                swing += 0.3;
                arm.rotation.z = originalRotation + Math.sin(swing) * 0.8;
                
                if (swing > Math.PI) {
                    arm.rotation.z = originalRotation;
                    clearInterval(swingInterval);
                }
            }, 20);
        } else if (type === 'enemy') {
            const head = model.userData.head;
            const originalY = head.position.y;
            
            head.position.y += 0.5;
            setTimeout(() => {
                head.position.y = originalY;
            }, 100);
        }
    }

    createDamageNumber(position, damage) {
        const canvas = document.createElement('canvas');
        canvas.width = 256;
        canvas.height = 256;
        const ctx = canvas.getContext('2d');
        
        ctx.fillStyle = '#ff4444';
        ctx.font = 'bold 80px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`-${damage}`, 128, 128);
        
        const texture = new THREE.CanvasTexture(canvas);
        const geometry = new THREE.PlaneGeometry(2, 2);
        const material = new THREE.MeshBasicMaterial({ map: texture, transparent: true });
        const sprite = new THREE.Mesh(geometry, material);
        
        sprite.position.copy(position);
        sprite.position.y += 2;
        this.scene.add(sprite);
        
        // Animation
        let frame = 0;
        const animate = () => {
            frame++;
            sprite.position.y += 0.1;
            sprite.material.opacity = 1 - (frame / 30);
            
            if (frame < 30) {
                requestAnimationFrame(animate);
            } else {
                this.scene.remove(sprite);
            }
        };
        animate();
    }

    createParticles(position, color) {
        for (let i = 0; i < 10; i++) {
            const particleGeometry = new THREE.SphereGeometry(0.1, 8, 8);
            const particleMaterial = new THREE.MeshBasicMaterial({ color });
            const particle = new THREE.Mesh(particleGeometry, particleMaterial);
            
            particle.position.copy(position);
            particle.velocity = new THREE.Vector3(
                (Math.random() - 0.5) * 2,
                Math.random() * 2,
                (Math.random() - 0.5) * 2
            );
            particle.life = 30;
            
            this.scene.add(particle);
            this.particleSystem.push(particle);
        }
    }

    updateHPBars() {
        const playerPercent = (this.player.hp / this.player.maxHp) * 100;
        const enemyPercent = (this.enemy.hp / this.enemy.maxHp) * 100;
        
        document.getElementById('player-hp-fill').style.width = playerPercent + '%';
        document.getElementById('enemy-hp-fill').style.width = enemyPercent + '%';
        document.getElementById('player-hp-text').textContent = `${this.player.hp}/${this.player.maxHp} HP`;
        document.getElementById('enemy-hp-text').textContent = `${this.enemy.hp}/${this.enemy.maxHp} HP`;
    }

    addBattleLog(text) {
        this.battleLog.unshift(text);
        if (this.battleLog.length > 5) this.battleLog.pop();
        
        const logDiv = document.getElementById('battle-log');
        logDiv.innerHTML = this.battleLog.map(log => `<div class="log-entry">${log}</div>`).join('');
    }

    endBattle(result) {
        this.gameState = result;
        
        if (result === 'victory') {
            document.getElementById('victory-screen').style.display = 'flex';
            this.playSound('victory');
        } else {
            document.getElementById('defeat-screen').style.display = 'flex';
            this.playSound('defeat');
        }
        
        document.getElementById('tap-btn').disabled = true;
    }

    playSound(type) {
        // Placeholder for sound effects
        console.log(`Playing sound: ${type}`);
    }

    onWindowResize() {
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(window.innerWidth, window.innerHeight);
    }

    animate = () => {
        requestAnimationFrame(this.animate);

        // Update particles
        for (let i = this.particleSystem.length - 1; i >= 0; i--) {
            const particle = this.particleSystem[i];
            particle.position.add(particle.velocity);
            particle.velocity.y -= 0.05; // gravity
            particle.life--;
            
            if (particle.life <= 0) {
                this.scene.remove(particle);
                this.particleSystem.splice(i, 1);
            }
        }

        // Animate dragon wings
        if (this.enemyModel) {
            this.enemyModel.userData.leftWing.rotation.z = Math.sin(Date.now() * 0.005) * 0.5;
            this.enemyModel.userData.rightWing.rotation.z = -Math.sin(Date.now() * 0.005) * 0.5;
        }

        // Camera orbit
        const time = Date.now() * 0.0003;
        this.camera.position.x = Math.sin(time) * 15;
        this.camera.position.z = Math.cos(time) * 15 + 10;
        this.camera.lookAt(0, 2, 0);

        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize Game
window.addEventListener('load', () => {
    new GameEngine();
});
