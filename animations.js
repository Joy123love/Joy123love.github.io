// ========================================
// STUNNING ANIMATIONS WITH GSAP + ANIME.JS
// ========================================

// Theme Toggle
const themeToggle = document.getElementById('themeToggle');
let isDark = false;
themeToggle.addEventListener('click', () => {
    isDark = !isDark;
    document.body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    themeToggle.textContent = isDark ? '' : '';
});

// Register GSAP ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Project data
const projects = {
    'achievement': { name: 'Achievement Unlocked!', description: 'You found the star tile!' },
    'swish-kunai': { name: 'Swish Kunai Game', description: 'A fun kunai throwing game with progressive difficulty' },
    'music-player': { name: 'Music Player', description: 'Beautiful music player with game mode' },
    'bonus': { name: 'Bonus Project', description: 'Special bonus content!' },
    '30-seconds': { name: '30 Seconds Game', description: 'Fast-paced word guessing game' }
};

// ========================================
// 1. TILES FLY IN FROM DIFFERENT DIRECTIONS
// ========================================
function animateTilesEntrance() {
    const tiles = document.querySelectorAll('.tile');

    // Set initial state (invisible and positioned off-screen)
    gsap.set(tiles, { opacity: 0, scale: 0 });

    // Animate each tile from different directions
    tiles.forEach((tile, index) => {
        const directions = [
            { x: -200, y: -200, rotation: -180 },  // Top-left
            { x: 200, y: -200, rotation: 180 },    // Top-right
            { x: -200, y: 200, rotation: 180 },    // Bottom-left
            { x: 200, y: 200, rotation: -180 },    // Bottom-right
            { x: 0, y: -200, rotation: 360 },      // Top-center
            { x: 0, y: 200, rotation: -360 }       // Bottom-center
        ];

        const dir = directions[index % directions.length];

        gsap.to(tile, {
            opacity: 1,
            scale: 1,
            x: 0,
            y: 0,
            rotation: 0,
            duration: 1.2,
            ease: 'back.out(1.7)',
            delay: index * 0.1 + 0.5, // Staggered delay
            startAt: {
                x: dir.x,
                y: dir.y,
                rotation: dir.rotation
            }
        });
    });
}

// ========================================
// 2. 3D TILT ON HOVER
// ========================================
function add3DTiltEffect() {
    const tiles = document.querySelectorAll('.tile');

    tiles.forEach(tile => {
        tile.addEventListener('mousemove', (e) => {
            const rect = tile.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 5;
            const rotateY = (centerX - x) / 5;

            gsap.to(tile, {
                rotationX: rotateX,
                rotationY: rotateY,
                transformPerspective: 1000,
                duration: 0.3,
                ease: 'power2.out'
            });
        });

        tile.addEventListener('mouseleave', () => {
            gsap.to(tile, {
                rotationX: 0,
                rotationY: 0,
                duration: 0.5,
                ease: 'elastic.out(1, 0.3)'
            });
        });
    });
}

// ========================================
// 3. WALKING ANIMATION FOR CHARACTER
// ========================================
function createWalkingAnimation() {
    const legLeft = document.querySelector('.leg-left');
    const legRight = document.querySelector('.leg-right');

    if (legLeft && legRight) {
        // Walking animation using Anime.js
        const walkTimeline = anime.timeline({
            loop: true,
            autoplay: false
        });

        walkTimeline
            .add({
                targets: legLeft,
                translateY: [0, -10, 0],
                duration: 300,
                easing: 'easeInOutQuad'
            })
            .add({
                targets: legRight,
                translateY: [0, -10, 0],
                duration: 300,
                easing: 'easeInOutQuad'
            }, '-=150');

        return walkTimeline;
    }
    return null;
}

// ========================================
// 4. CHARACTER MOVEMENT TO TILE
// ========================================
function moveCharacterToTile(tile, walkAnimation) {
    const character = document.getElementById('character');
    const tileRect = tile.getBoundingClientRect();
    const containerRect = document.querySelector('.path-container').getBoundingClientRect();

    const newTop = tileRect.top - containerRect.top + tileRect.height / 2 - 50;
    const newLeft = tileRect.left - containerRect.left + tileRect.width / 2 - 40;

    // Start walking animation
    if (walkAnimation) walkAnimation.play();

    // Move character with GSAP
    gsap.to(character, {
        top: newTop,
        left: newLeft,
        duration: 1,
        ease: 'power2.inOut',
        onComplete: () => {
            // Stop walking
            if (walkAnimation) walkAnimation.pause();

            // Celebration jump
            gsap.to(character, {
                y: -20,
                duration: 0.3,
                yoyo: true,
                repeat: 1,
                ease: 'power2.out'
            });
        }
    });
}

// ========================================
// 5. SCROLL FADE-IN ANIMATIONS
// ========================================
function setupScrollAnimations() {
    // Fade in elements as you scroll
    gsap.utils.toArray('.tile, .progress-stars').forEach(element => {
        gsap.fromTo(element,
            { opacity: 0, y: 50 },
            {
                opacity: 1,
                y: 0,
                duration: 0.8,
                scrollTrigger: {
                    trigger: element,
                    start: 'top 90%',
                    end: 'top 60%',
                    scrub: 1,
                    toggleActions: 'play none none reverse'
                }
            }
        );
    });
}

// ========================================
// 6. TILE CLICK EFFECTS
// ========================================
function setupTileClickEffects() {
    const tiles = document.querySelectorAll('.tile');
    const walkAnimation = createWalkingAnimation();

    tiles.forEach(tile => {
        tile.addEventListener('click', function () {
            const projectId = this.dataset.project;
            const project = projects[projectId];

            // Explosive scale animation
            gsap.timeline()
                .to(this, {
                    scale: 1.3,
                    duration: 0.2,
                    ease: 'power2.out'
                })
                .to(this, {
                    scale: 1,
                    duration: 0.3,
                    ease: 'elastic.out(1, 0.3)'
                });

            // Rotate animation
            anime({
                targets: this,
                rotate: [0, 360],
                duration: 600,
                easing: 'easeInOutQuad'
            });

            // Show success message
            showSuccessMessage(project);

            // Move character
            moveCharacterToTile(this, walkAnimation);

            // Console log
            console.log('Tile clicked:', projectId);
            console.log('Test result: true');
        });
    });
}

// ========================================
// SUCCESS MESSAGE
// ========================================
function showSuccessMessage(project) {
    const existing = document.querySelector('.success-message');
    if (existing) existing.remove();

    const message = document.createElement('div');
    message.className = 'success-message';
    message.innerHTML = `
        <h2>✨ ${project.name}</h2>
        <p>${project.description}</p>
        <p style="margin-top: 20px; color: #4CAF50; font-weight: bold;">Test: TRUE ✓</p>
    `;

    document.body.appendChild(message);

    // Animate in with GSAP
    gsap.fromTo(message,
        { scale: 0, opacity: 0, rotation: -180 },
        { scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: 'back.out(1.7)' }
    );

    // Animate out after 3 seconds
    setTimeout(() => {
        gsap.to(message, {
            scale: 0,
            opacity: 0,
            rotation: 180,
            duration: 0.3,
            ease: 'back.in(1.7)',
            onComplete: () => message.remove()
        });
    }, 3000);
}

// ========================================
// INITIALIZE ALL ANIMATIONS
// ========================================
window.addEventListener('DOMContentLoaded', () => {
    console.log('🎨 Initializing stunning animations...');

    // Wait a bit for page to fully load
    setTimeout(() => {
        animateTilesEntrance();
        add3DTiltEffect();
        setupScrollAnimations();
        setupTileClickEffects();

        console.log('✨ All animations loaded!');
        console.log('📱 Click any tile to see the magic!');
    }, 100);
});

// Character idle breathing animation
gsap.to('#character', {
    scale: 1.02,
    duration: 2,
    repeat: -1,
    yoyo: true,
    ease: 'sine.inOut'
});
