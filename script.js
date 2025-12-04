// Settings Overlay - Initialize after DOM is ready
let settingsBtn, settingsOverlay, settingsThemeToggle, playPauseBtn, volumeSlider, volumeValue;
let menuBtn, menuOverlay;

let isGradientTheme = false;
let isPlaying = false;
let currentVolume = 50;

// Create audio element for the song - starts paused
const audio = new Audio('Theme from a summer place (Percy Faith version).mp3');
audio.volume = currentVolume / 100;
audio.loop = true; // Loop the song
audio.pause(); // Ensure it starts paused

// Initialize settings when DOM is ready
function initSettings() {
    if (!settingsBtn || !settingsOverlay) return;
    settingsBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        settingsOverlay.classList.toggle('open');
    });

    // Close overlay when clicking outside
    document.addEventListener('click', (e) => {
        if (settingsOverlay && settingsOverlay.classList.contains('open') &&
            !settingsOverlay.contains(e.target) &&
            settingsBtn && !settingsBtn.contains(e.target)) {
            settingsOverlay.classList.remove('open');
        }
    });
}

// Initialize theme toggle
function initThemeToggle() {
    if (!settingsThemeToggle) return;
    settingsThemeToggle.addEventListener('click', () => {
        isGradientTheme = !isGradientTheme;
        // Add morphing class for smoother color transition
        document.body.classList.add('theme-morphing');

        // Toggle gradient background theme
        document.body.classList.toggle('gradient-theme', isGradientTheme);
        settingsThemeToggle.textContent = isGradientTheme ? '☀️' : '🌙';

        // Remove morphing class after transition completes
        setTimeout(() => {
            document.body.classList.remove('theme-morphing');
        }, 2000); // Match CSS transition duration
    });
}

// Initialize play/pause button
function initPlayPause() {
    if (!playPauseBtn) return;
    playPauseBtn.addEventListener('click', () => {
        isPlaying = !isPlaying;
        playPauseBtn.classList.toggle('playing', isPlaying);

        if (isPlaying) {
            audio.play().catch(error => {
                console.error('Error playing audio:', error);
                // If autoplay is blocked, reset the state
                isPlaying = false;
                playPauseBtn.classList.remove('playing');
            });
        } else {
            audio.pause();
        }
    });

    // Update button state when audio ends (shouldn't happen with loop, but just in case)
    audio.addEventListener('ended', () => {
        isPlaying = false;
        playPauseBtn.classList.remove('playing');
    });

    // Handle audio errors
    audio.addEventListener('error', (e) => {
        console.error('Audio error:', e);
        isPlaying = false;
        playPauseBtn.classList.remove('playing');
    });
}

// Initialize volume slider
function initVolumeSlider() {
    if (!volumeSlider || !volumeValue) return;
    // Set initial volume display
    volumeValue.textContent = `${currentVolume}%`;

    volumeSlider.addEventListener('input', (e) => {
        currentVolume = e.target.value;
        volumeValue.textContent = `${currentVolume}%`;
        audio.volume = currentVolume / 100;
    });
}

// Initialize menu overlay
function initMenuOverlay() {
    if (!menuBtn || !menuOverlay) return;
    function positionMenuOverlay() {
        const btnRect = menuBtn.getBoundingClientRect();
        menuOverlay.style.top = `${btnRect.bottom + 10}px`;
        menuOverlay.style.right = `${window.innerWidth - btnRect.right}px`;
    }

    // Position overlay on load and resize
    positionMenuOverlay();
    window.addEventListener('resize', positionMenuOverlay);

    menuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        positionMenuOverlay(); // Reposition before opening
        menuOverlay.classList.toggle('open');
    });

    // Close overlay when clicking outside
    document.addEventListener('click', (e) => {
        if (menuOverlay.classList.contains('open') &&
            !menuOverlay.contains(e.target) &&
            !menuBtn.contains(e.target)) {
            menuOverlay.classList.remove('open');
        }
    });
}

// Function to check checkbox when tile is clicked
function checkProjectCheckbox(projectId) {
    const checkboxId = `check-${projectId}`;
    const checkbox = document.getElementById(checkboxId);
    if (checkbox) {
        checkbox.checked = true;
    }
}

// Project data for all tiles
const projects = {
    'simple-html': {
        name: 'Simple HTML Basics',
        description: 'My first HTML project - A personal introduction page',
        projectNumber: 1,
        overlayContent: `
            <div class="project-header">
                <h2>Simple HTML Basics</h2>
            </div>
            <div class="project-embed-container">
                <iframe src="simple_html_app/index.html" class="project-iframe" frameborder="0" scrolling="auto"></iframe>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>This was my very first HTML project! It's a personal introduction page that I created while learning the fundamentals of web development. The page includes basic HTML elements like headers, paragraphs, lists, and images.</p>
                <p>Through this project, I learned how to structure an HTML document, use semantic HTML tags, and create a simple but functional webpage. It represents the beginning of my journey into web development and coding.</p>
                <p><strong>Technologies Used:</strong></p>
                <div class="tech-buttons">
                    <span class="tech-button">HTML5</span>
                    <span class="tech-button">CSS</span>
                </div>
                <p><strong>Key Learning:</strong> Understanding HTML document structure, semantic elements, and creating my first interactive web page.</p>
            </div>
        `
    },
    'todo-app': {
        name: 'To-Do App 2023',
        description: 'A modern task management application',
        projectNumber: 2,
        overlayContent: `
            <div class="project-header">
                <h2>To-Do App 2023</h2>
            </div>
            <div class="project-embed-container">
                <iframe src="to do 2023/index.html" class="project-iframe" frameborder="0" scrolling="auto"></iframe>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>A responsive to-do list application that lets users add, complete, and delete tasks with persistent state.</p>
                <p><strong>Technologies Used:</strong></p>
                <div class="tech-buttons">
                    <span class="tech-button">HTML5</span>
                    <span class="tech-button">CSS</span>
                    <span class="tech-button">JavaScript</span>
                </div>
                <p><strong>Key Learning:</strong> Managing DOM state, handling user interactions, and creating accessible form experiences.</p>
            </div>
        `
    },
    'password-generator': {
        name: 'Password Generator',
        description: 'Generate secure passwords with custom options',
        projectNumber: 3,
        overlayContent: `
            <div class="project-header">
                <h2>Password Generator</h2>
            </div>
            <div class="project-embed-container">
                <div class="slideshow-window">
                    <img id="slideshow-password-generator" src="" alt="Password Generator slideshow" class="slideshow-img" />
                </div>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>A Python-based password generator with SQLite database integration for secure password storage and management.</p>
                <p>This slideshow showcases the application interface and code implementation.</p>
            </div>
        `
    },
    '30-seconds': {
        name: '30 Seconds Game',
        description: 'Fast-paced word guessing game',
        projectNumber: 4,
        overlayContent: `
            <div class="project-header">
                <h2>30 Seconds Game</h2>
            </div>
            <div class="project-embed-container">
                <div class="slideshow-window">
                    <img id="slideshow-30-seconds" src="" alt="30 Seconds Game slideshow" />
                </div>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>A fast-paced word guessing game where you have 30 seconds to complete quick challenges.</p>
                <p>This panel showcases a slideshow of screenshots and moments from the game instead of running the app directly.</p>
                <p><strong>Note:</strong> Replace the image paths in <code>slideshow30Images</code> (in <code>script.js</code>) with your actual uploaded image files.</p>
            </div>
        `
    },
    'swish-kunai': {
        name: 'Swish Kunai',
        description: 'A fun ninja throwing game',
        projectNumber: 5,
        overlayContent: `
            <div class="project-header">
                <h2>Swish Kunai</h2>
            </div>
            <div class="project-embed-container">
                <div class="slideshow-window">
                    <img id="slideshow-swish-kunai" src="" alt="Swish Kunai slideshow" class="slideshow-img" />
                </div>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>A fun ninja throwing game with fluid movement and combat mechanics, featuring a music player interface.</p>
                <p>This slideshow showcases the game interface and code implementation.</p>
            </div>
        `
    },
    'aves-derivative': {
        name: 'Aves Derivative',
        description: 'An experimental project',
        projectNumber: 6,
        overlayContent: `
            <div class="project-header">
                <h2>Aves Derivative</h2>
            </div>
            <div class="project-embed-container">
                <div class="slideshow-window">
                    <img id="slideshow-aves-derivative" src="" alt="Aves Derivative slideshow" class="slideshow-img" />
                </div>
            </div>
            <div class="project-description">
                <h3>About This Project</h3>
                <p>An experimental project exploring advanced visualization techniques and data representation with over 1,300 files.</p>
                <p>This slideshow showcases key moments and implementations from the project.</p>
            </div>
        `
    }
};

// Get all tiles - initialize after DOM is ready
let tiles, character, pathContainer;

// Drag-to-move character with mouse
let isDraggingCharacter = false;
let dragOffsetX = 0;
let dragOffsetY = 0;
let charPosX = null;
let charPosY = null;
let followTargetX = null;
let followTargetY = null;
const CHARACTER_FOLLOW_DISTANCE = 80; // horizontal gap between cursor and character
const CHARACTER_FOLLOW_SMOOTHING = 0.05;
const CHARACTER_MAX_STEP = 4; // max pixels per frame to prevent fast jumps

// Slideshow configuration for Password Generator (tile 3)
const slideshowPasswordImages = [
    'media/project3/Password Generator 12_4_2025 10_27_16 AM.png',
    'media/project3/main.py - Coding portfolio 1 - Cursor 12_4_2025 10_28_04 AM.png',
    'media/project3/main.py - Coding portfolio 1 - Cursor 12_4_2025 10_28_37 AM.png'
];
let slideshowPasswordIndex = 0;
let slideshowPasswordInterval = null;

// Slideshow configuration for 30 Seconds Game (tile 4)
const slideshow30Images = [
    'media/project4/30 Seconds Game 12_4_2025 10_13_47 AM.png',
    'media/project4/30 Seconds Game 12_4_2025 10_15_08 AM.png',
    'media/project4/30 Seconds Game 12_4_2025 10_19_13 AM.png',
    'media/project4/script.js - Coding portfolio 1 - Cursor 12_4_2025 10_17_24 AM.png'
];
let slideshow30Index = 0;
let slideshow30Interval = null;

// Slideshow configuration for Swish Kunai (tile 5)
const slideshowSwishImages = [
    'media/project5/Swish Kunai 12_4_2025 11_59_25 AM.png',
    'media/project5/Swish Kunai 12_4_2025 11_59_39 AM.png',
    'media/project5/Coding portfolio 1 - Antigravity - music_player_window.py 4_12_2025 12_31_08.png'
];
let slideshowSwishIndex = 0;
let slideshowSwishInterval = null;

// Slideshow configuration for Aves Derivative (tile 6)
const slideshowAvesImages = [
    'media/project6/1.png',
    'media/project6/aves-gallery-1.jpg',
    'media/project6/main.py - Coding portfolio 1 - Cursor 12_4_2025 10_41_31 AM.png'
];
let slideshowAvesIndex = 0;
let slideshowAvesInterval = null;

// Generic slideshow function with slide animation
function startSlideshow(imgElementId, images, indexVar, intervalVar) {
    const imgEl = document.getElementById(imgElementId);
    if (!imgEl || !images.length) return;

    // Reset index and show first image
    let currentIndex = 0;
    imgEl.src = images[currentIndex];
    imgEl.classList.remove('slide-in');
    // Trigger reflow
    void imgEl.offsetWidth;
    imgEl.classList.add('slide-in');

    // Clear any existing interval
    if (window[intervalVar]) {
        clearInterval(window[intervalVar]);
    }

    // Cycle through images with slide animation
    window[intervalVar] = setInterval(() => {
        nextSlide(imgElementId, images, indexVar, intervalVar);
    }, 3000); // change image every 3s

    return window[intervalVar];
}

// Helper to advance to next slide
function nextSlide(imgElementId, images, indexVar, intervalVar) {
    const imgEl = document.getElementById(imgElementId);
    if (!imgEl) return;

    // Get current index from window scope variable name
    // Note: We need to access the variable by name string
    let currentIndex = window[indexVar] || 0;

    // Add slide-out class (move to left)
    imgEl.classList.remove('slide-in', 'slide-in-left');
    imgEl.classList.add('slide-out');

    // Wait for slide-out animation, then change image
    setTimeout(() => {
        currentIndex = (currentIndex + 1) % images.length;
        // Update global index variable
        window[indexVar] = currentIndex;

        imgEl.src = images[currentIndex];

        // Add slide-in class (enter from right)
        imgEl.classList.remove('slide-out', 'slide-out-right');
        imgEl.classList.add('slide-in');
    }, 400);
}

// Helper to go to previous slide
function prevSlide(imgElementId, images, indexVar, intervalVar) {
    const imgEl = document.getElementById(imgElementId);
    if (!imgEl) return;

    let currentIndex = window[indexVar] || 0;

    // Add slide-out-right class (move to right)
    imgEl.classList.remove('slide-in', 'slide-in-left');
    imgEl.classList.add('slide-out-right');

    // Wait for slide-out animation, then change image
    setTimeout(() => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        // Update global index variable
        window[indexVar] = currentIndex;

        imgEl.src = images[currentIndex];

        // Add slide-in-left class (enter from left)
        imgEl.classList.remove('slide-out', 'slide-out-right');
        imgEl.classList.add('slide-in-left');
    }, 400);
}

// Setup swipe gestures for slideshow
function setupSwipeGestures(elementId, images, indexVar, intervalVar) {
    const element = document.getElementById(elementId);
    if (!element) return;

    let touchStartX = 0;
    let touchEndX = 0;
    let isDragging = false;
    let startX = 0;

    // Touch events
    element.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
        // Pause slideshow on interaction
        if (window[intervalVar]) clearInterval(window[intervalVar]);
    }, { passive: true });

    element.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
        // Restart slideshow
        window[intervalVar] = setInterval(() => {
            nextSlide(elementId, images, indexVar, intervalVar);
        }, 3000);
    }, { passive: true });

    // Mouse events
    element.addEventListener('mousedown', (e) => {
        isDragging = true;
        startX = e.clientX;
        e.preventDefault(); // Prevent image drag default behavior
        // Pause slideshow on interaction
        if (window[intervalVar]) clearInterval(window[intervalVar]);
    });

    element.addEventListener('mouseup', (e) => {
        if (!isDragging) return;
        isDragging = false;
        const endX = e.clientX;
        const diffX = endX - startX;

        if (Math.abs(diffX) > 50) { // Threshold
            if (diffX > 0) {
                prevSlide(elementId, images, indexVar, intervalVar);
            } else {
                nextSlide(elementId, images, indexVar, intervalVar);
            }
        }

        // Restart slideshow
        window[intervalVar] = setInterval(() => {
            nextSlide(elementId, images, indexVar, intervalVar);
        }, 3000);
    });

    element.addEventListener('mouseleave', () => {
        if (isDragging) {
            isDragging = false;
            // Restart slideshow if mouse leaves
            if (!window[intervalVar]) {
                window[intervalVar] = setInterval(() => {
                    nextSlide(elementId, images, indexVar, intervalVar);
                }, 3000);
            }
        }
    });

    function handleSwipe() {
        const diffX = touchEndX - touchStartX;
        if (Math.abs(diffX) > 50) { // Threshold
            if (diffX > 0) {
                // Swipe Right -> Previous Image
                prevSlide(elementId, images, indexVar, intervalVar);
            } else {
                // Swipe Left -> Next Image
                nextSlide(elementId, images, indexVar, intervalVar);
            }
        }
    }
}

function startPasswordSlideshow() {
    slideshowPasswordInterval = startSlideshow('slideshow-password-generator', slideshowPasswordImages, 'slideshowPasswordIndex', 'slideshowPasswordInterval');
}

function start30SecondsSlideshow() {
    slideshow30Interval = startSlideshow('slideshow-30-seconds', slideshow30Images, 'slideshow30Index', 'slideshow30Interval');
    setupSwipeGestures('slideshow-30-seconds', slideshow30Images, 'slideshow30Index', 'slideshow30Interval');
}

function startSwishSlideshow() {
    slideshowSwishInterval = startSlideshow('slideshow-swish-kunai', slideshowSwishImages, 'slideshowSwishIndex', 'slideshowSwishInterval');
}

function startAvesSlideshow() {
    slideshowAvesInterval = startSlideshow('slideshow-aves-derivative', slideshowAvesImages, 'slideshowAvesIndex', 'slideshowAvesInterval');
}

// Initialize character dragging/following - must be called after DOM is ready
function initCharacterMovement() {
    if (!character || !pathContainer) return;

    // Initialise character position relative to container
    const initRect = character.getBoundingClientRect();
    const containerRect = pathContainer.getBoundingClientRect();
    charPosX = initRect.left - containerRect.left;
    charPosY = initRect.top - containerRect.top;

    // Mouse move inside the path container: update follow target
    pathContainer.addEventListener('mousemove', (e) => {
        const rect = pathContainer.getBoundingClientRect();
        followTargetX = e.clientX - rect.left;
        followTargetY = e.clientY - rect.top;
    });

    // Hover-follow animation loop
    function updateCharacterFollow() {
        if (!isDraggingCharacter && followTargetX != null && followTargetY != null) {
            const rect = pathContainer.getBoundingClientRect();
            const charRect = character.getBoundingClientRect();

            const charWidth = charRect.width;
            const charHeight = charRect.height;
            const containerWidth = rect.width;
            const containerHeight = rect.height;

            // Desired position: to the left of the cursor, with a fixed horizontal gap
            let targetX = followTargetX - CHARACTER_FOLLOW_DISTANCE - charWidth / 2;
            let targetY = followTargetY - charHeight / 2;

            // Clamp within container margins
            const margin = 8;
            const minX = margin;
            const maxX = containerWidth - charWidth - margin;
            const minY = margin;
            // Prevent character from going into bottom panel (10vh)
            const panelHeight = window.innerHeight * 0.1;
            const containerBottom = rect.bottom;
            const viewportBottom = window.innerHeight;
            const availableHeight = containerBottom - rect.top - panelHeight - (viewportBottom - containerBottom);
            const maxY = Math.min(containerHeight - charHeight - margin, availableHeight - charHeight - margin);

            targetX = Math.min(Math.max(targetX, minX), maxX);
            targetY = Math.min(Math.max(targetY, minY), maxY);

            let stepX = (targetX - charPosX) * CHARACTER_FOLLOW_SMOOTHING;
            let stepY = (targetY - charPosY) * CHARACTER_FOLLOW_SMOOTHING;

            // Clamp maximum movement per frame so the character never moves too fast
            stepX = Math.max(Math.min(stepX, CHARACTER_MAX_STEP), -CHARACTER_MAX_STEP);
            stepY = Math.max(Math.min(stepY, CHARACTER_MAX_STEP), -CHARACTER_MAX_STEP);

            charPosX += stepX;
            charPosY += stepY;

            character.style.left = `${charPosX}px`;
            character.style.top = `${charPosY}px`;
            character.style.transform = 'none';
        }

        requestAnimationFrame(updateCharacterFollow);
    }

    requestAnimationFrame(updateCharacterFollow);

    character.addEventListener('mousedown', (e) => {
        isDraggingCharacter = true;
        character.classList.add('dragging');

        const rect = character.getBoundingClientRect();
        dragOffsetX = e.clientX - rect.left;
        dragOffsetY = e.clientY - rect.top;

        e.preventDefault();
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDraggingCharacter) return;

        const containerRect = pathContainer.getBoundingClientRect();
        const characterRect = character.getBoundingClientRect();

        // Prevent character from going into bottom panel (10vh)
        const panelHeight = window.innerHeight * 0.1;
        const containerBottom = containerRect.bottom;
        const viewportBottom = window.innerHeight;
        const availableHeight = containerBottom - containerRect.top - panelHeight - (viewportBottom - containerBottom);
        const maxY = Math.min(containerRect.height - characterRect.height - 8, availableHeight - characterRect.height - 8);

        const newLeft = Math.max(8, Math.min(e.clientX - containerRect.left - dragOffsetX, containerRect.width - characterRect.width - 8));
        const newTop = Math.max(8, Math.min(e.clientY - containerRect.top - dragOffsetY, maxY));

        character.style.left = `${newLeft}px`;
        character.style.top = `${newTop}px`;
        character.style.transform = 'none';

        charPosX = newLeft;
        charPosY = newTop;
    });

    document.addEventListener('mouseup', () => {
        if (!isDraggingCharacter) return;
        isDraggingCharacter = false;
        character.classList.remove('dragging');
    });
}

// Panel state management - now creates separate panels for each project
const panelManager = {
    panels: {},
    currentOpenPanel: null,

    // Initialize panels for all projects
    init() {
        // Create a panel for each project
        Object.keys(projects).forEach(projectId => {
            const project = projects[projectId];

            // Create panel element
            const panelEl = document.createElement('div');
            panelEl.id = `panel-${projectId}`;
            panelEl.className = 'detail-panel';
            panelEl.innerHTML = `
                <button class="detail-close">×</button>
                <div class="detail-content">
                    ${project.overlayContent}
                </div>
            `;

            document.body.appendChild(panelEl);

            // Store reference
            this.panels[projectId] = {
                element: panelEl,
                closeBtn: panelEl.querySelector('.detail-close'),
                content: panelEl.querySelector('.detail-content')
            };

            // Add close button listener
            this.panels[projectId].closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.close(projectId);
            });
        });

        // Add outside click listener
        document.addEventListener('click', (e) => {
            if (this.currentOpenPanel &&
                !this.panels[this.currentOpenPanel].element.contains(e.target) &&
                !e.target.closest('.tile')) {
                this.close(this.currentOpenPanel);
            }
        });
    },

    // Open a specific panel
    open(projectId) {
        const panel = this.panels[projectId];
        if (!panel) return;

        // If already open, just ensure it stays open and scrolls to top / restarts animations
        if (this.currentOpenPanel === projectId && panel.element.classList.contains('open')) {
            // Panel already open - reset scroll and ensure visibility
            if (panel.content) {
                panel.content.scrollTop = 0;
                panel.content.style.opacity = '1';

                // Restart auto-scroll for panel 1 (simple-html) and 2 (todo-app)
                if (projectId === 'simple-html' || projectId === 'todo-app') {
                    this.autoScrollPanel(panel.content);
                }

                // Restart auto-scroll for panel 3 (password-generator), 4 (30-seconds), 5 (swish-kunai), and 6 (aves-derivative) with 6s delay
                if (projectId === 'password-generator' || projectId === '30-seconds' || projectId === 'swish-kunai' || projectId === 'aves-derivative') {
                    this.autoScrollPanel(panel.content, 6000);
                }

                // Restart slideshows
                if (projectId === 'password-generator') {
                    startPasswordSlideshow();
                }
                if (projectId === '30-seconds') {
                    start30SecondsSlideshow();
                }
                if (projectId === 'swish-kunai') {
                    startSwishSlideshow();
                }
                if (projectId === 'aves-derivative') {
                    startAvesSlideshow();
                }
            }
            return;
        }

        // Close any currently open panel
        if (this.currentOpenPanel && this.currentOpenPanel !== projectId) {
            this.close(this.currentOpenPanel);
        }

        // Open the new panel
        document.body.classList.add('panel-open');
        panel.element.classList.add('open');
        this.currentOpenPanel = projectId;

        // Fade in content
        setTimeout(() => {
            if (panel.content) {
                panel.content.style.opacity = '1';
                panel.content.scrollTop = 0; // Always start from top

                // Auto-scroll for panel 1 (simple-html project) and 2 (todo-app)
                if (projectId === 'simple-html' || projectId === 'todo-app') {
                    this.autoScrollPanel(panel.content);
                }

                // Auto-scroll for panel 3 (password-generator), 4 (30-seconds), 5 (swish-kunai), and 6 (aves-derivative) with 6s delay
                if (projectId === 'password-generator' || projectId === '30-seconds' || projectId === 'swish-kunai' || projectId === 'aves-derivative') {
                    this.autoScrollPanel(panel.content, 6000);
                }

                // Start slideshows
                if (projectId === 'password-generator') {
                    startPasswordSlideshow();
                }
                if (projectId === '30-seconds') {
                    start30SecondsSlideshow();
                }
                if (projectId === 'swish-kunai') {
                    startSwishSlideshow();
                }
                if (projectId === 'aves-derivative') {
                    startAvesSlideshow();
                }
            }
        }, 50);
    },

    // Auto-scroll function for panel content
    autoScrollPanel(contentElement, initialDelay = 500) {
        if (!contentElement) return;

        // Reset scroll position to top first
        contentElement.scrollTop = 0;

        // Wait a bit for the panel to fully open, then start scrolling
        setTimeout(() => {
            const scrollDuration = 10000; // 10 seconds to scroll (slower)
            const scrollHeight = contentElement.scrollHeight - contentElement.clientHeight;
            const scrollStep = scrollHeight / (scrollDuration / 16); // 60fps = 16ms per frame
            let currentScroll = 0;

            const scrollInterval = setInterval(() => {
                currentScroll += scrollStep;

                if (currentScroll >= scrollHeight) {
                    contentElement.scrollTop = scrollHeight;
                    clearInterval(scrollInterval);
                } else {
                    contentElement.scrollTop = currentScroll;
                }
            }, 16); // ~60fps
        }, initialDelay); // Use custom delay (default 500ms)
    },

    // Close a specific panel
    close(projectId) {
        const panel = this.panels[projectId];
        if (!panel) return;

        // Fade out content
        if (panel.content) {
            panel.content.style.opacity = '0';
        }

        setTimeout(() => {
            panel.element.classList.remove('open');
            document.body.classList.remove('panel-open');

            // Stop slideshows when closing panels
            if (projectId === 'password-generator' && slideshowPasswordInterval) {
                clearInterval(slideshowPasswordInterval);
                slideshowPasswordInterval = null;
            }
            if (projectId === '30-seconds' && slideshow30Interval) {
                clearInterval(slideshow30Interval);
                slideshow30Interval = null;
            }
            if (projectId === 'swish-kunai' && slideshowSwishInterval) {
                clearInterval(slideshowSwishInterval);
                slideshowSwishInterval = null;
            }
            if (projectId === 'aves-derivative' && slideshowAvesInterval) {
                clearInterval(slideshowAvesInterval);
                slideshowAvesInterval = null;
            }

            if (this.currentOpenPanel === projectId) {
                this.currentOpenPanel = null;
            }
        }, 200);
    }
};

// Initialize panel manager when DOM is ready (moved to DOMContentLoaded event)

// Open detail panel (now using the panel manager)
function openDetailPanel(project, projectId) {
    panelManager.open(projectId);
}

// Close detail panel (now using the panel manager)
function closeDetailPanel() {
    if (panelManager.currentOpenPanel) {
        panelManager.close(panelManager.currentOpenPanel);
        isPanelOpen = false;
        currentOpenTileId = null;
    }
}

// Close button handler is now part of the panel object

// Overlay only closes when close button is pressed - no clicking outside to close

// Function to initialize conversation clouds - positioned above tiles
function initConversationClouds() {
    console.log('Initializing conversation clouds...');
    const tiles = document.querySelectorAll('.tile');
    console.log(`Found ${tiles.length} tiles`);

    // Create tooltip container if it doesn't exist
    let tooltipContainer = document.querySelector('.tooltip-container');
    if (!tooltipContainer) {
        console.log('Creating tooltip container');
        tooltipContainer = document.createElement('div');
        tooltipContainer.className = 'tooltip-container';
        document.body.appendChild(tooltipContainer);
    } else {
        console.log('Tooltip container already exists');
    }

    tiles.forEach((tile, index) => {
        // Skip if already initialized (check for data attribute)
        if (tile.hasAttribute('data-tooltip-initialized')) {
            console.log(`Tile ${index + 1} already has tooltip initialized, skipping`);
            return;
        }

        // Mark as initialized
        tile.setAttribute('data-tooltip-initialized', 'true');
        console.log(`Setting up tile ${index + 1}`);
        let tooltip = null;
        let hideTimeout = null;
        let isHovering = false;

        // Create tooltip element
        function createTooltip() {
            if (tooltip) {
                return;
            }

            const projectId = tile.getAttribute('data-project');
            const project = projects[projectId];

            if (!project) {
                console.error('Project not found:', projectId);
                return;
            }

            tooltip = document.createElement('div');
            tooltip.className = 'tile-tooltip';
            tooltip.innerHTML = `
                <div class="tile-tooltip-title">${project.name}</div>
                <div class="tile-tooltip-body">${project.description}</div>
            `;

            tooltip.style.position = 'fixed';
            tooltip.style.opacity = '0';
            tooltip.style.visibility = 'hidden';
            tooltip.style.transform = 'translateY(10px)';

            tooltipContainer.appendChild(tooltip);

            // Position above tile
            positionTooltipAboveTile(tile, tooltip);

            // Force reflow to trigger the transition
            void tooltip.offsetWidth;

            // Apply visible styles
            tooltip.style.opacity = '1';
            tooltip.style.visibility = 'visible';
            tooltip.style.transform = 'translateY(0)';

            console.log('Tooltip created for tile:', projectId);
        }

        // Position tooltip above tile
        function positionTooltipAboveTile(tileElement, tooltipElement) {
            if (!tileElement || !tooltipElement) {
                return;
            }

            const tileRect = tileElement.getBoundingClientRect();
            tooltipElement.style.display = 'block';
            const tooltipRect = tooltipElement.getBoundingClientRect();

            // Position above the tile
            let top = tileRect.top - tooltipRect.height - 12; // 12px gap above tile
            let left = tileRect.left + (tileRect.width / 2) - (tooltipRect.width / 2);

            // Adjust if tooltip goes off screen horizontally
            if (left < 10) left = 10;
            if (left + tooltipRect.width > window.innerWidth - 10) {
                left = window.innerWidth - tooltipRect.width - 10;
            }

            // Adjust if tooltip goes off screen vertically (position below tile instead)
            if (top < 10) {
                top = tileRect.bottom + 12; // Position below tile if no space above
            }

            tooltipElement.style.top = `${top + window.scrollY}px`;
            tooltipElement.style.left = `${left}px`;
        }

        // Remove tooltip
        function removeTooltip() {
            if (!tooltip) return;

            tooltip.style.opacity = '0';
            tooltip.style.transform = 'translateY(10px)';

            setTimeout(() => {
                if (tooltip && tooltip.parentNode) {
                    tooltip.parentNode.removeChild(tooltip);
                }
                tooltip = null;
            }, 300);
        }

        // Mouse enter handler
        tile.addEventListener('mouseenter', (e) => {
            console.log('Mouse enter tile');
            isHovering = true;
            if (hideTimeout) {
                clearTimeout(hideTimeout);
                hideTimeout = null;
            }
            createTooltip();
        });

        // Mouse leave handler
        tile.addEventListener('mouseleave', () => {
            console.log('Mouse leave tile');
            isHovering = false;
            hideTimeout = setTimeout(() => {
                if (!isHovering) {
                    removeTooltip();
                }
            }, 300);
        });

        // Keep tooltip positioned correctly when mouse moves
        tile.addEventListener('mousemove', (e) => {
            if (tooltip) {
                if (hideTimeout) {
                    clearTimeout(hideTimeout);
                    hideTimeout = null;
                }
                positionTooltipAboveTile(tile, tooltip);
            }
        });
    });

    console.log('Finished initializing conversation clouds');
}

// Initialize conversation clouds - will be called after tiles are initialized

// Panel state tracking
let isPanelOpen = false;
let currentOpenTileId = null;

// Initialize tile click handlers - must be called after DOM is ready
function initTileHandlers() {
    document.querySelectorAll('.tile').forEach(tile => {
        tile.addEventListener('click', function () {
            const projectId = this.dataset.project;
            const project = projects[projectId];

            // Add click animation
            this.classList.add('clicked');
            setTimeout(() => this.classList.remove('clicked'), 500);

            // If same tile clicked and already open, do nothing (don't close)
            if (isPanelOpen && currentOpenTileId === projectId) {
                // Same tile clicked - keep it open, don't close
                return;
            }

            // Open/switch panel
            openDetailPanel(project, projectId);
            isPanelOpen = true;
            currentOpenTileId = projectId;

            // Move character to tile only when opening
            if (typeof moveCharacterToTile === 'function') {
                moveCharacterToTile(this);
            }

            // Check the corresponding checkbox in menu overlay
            checkProjectCheckbox(projectId);

            // Console log for testing
            console.log('Tile clicked:', projectId);
            console.log('Test result: true');
        });
    });
}

// Success message function removed - no popups except conversation clouds

// Move character to tile
function moveCharacterToTile(tile) {
    const tileRect = tile.getBoundingClientRect();
    const containerRect = document.querySelector('.path-container').getBoundingClientRect();
    const characterRect = character.getBoundingClientRect();

    // Prevent character from going into bottom panel (10vh)
    const panelHeight = window.innerHeight * 0.1;
    const containerBottom = containerRect.bottom;
    const viewportBottom = window.innerHeight;
    const availableHeight = containerBottom - containerRect.top - panelHeight - (viewportBottom - containerBottom);
    const maxY = Math.min(containerRect.height - characterRect.height - 8, availableHeight - characterRect.height - 8);

    let newTop = tileRect.top - containerRect.top + tileRect.height / 2 - 50;
    const newLeft = tileRect.left - containerRect.left + tileRect.width / 2 - 40;

    // Clamp to prevent going into panel
    newTop = Math.max(8, Math.min(newTop, maxY));

    character.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
    character.style.top = `${newTop}px`;
    character.style.left = `${newLeft}px`;
    character.style.transform = 'none';

    charPosX = newLeft;
    charPosY = newTop;
}

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        const focusedTile = document.activeElement;
        if (focusedTile.classList.contains('tile')) {
            focusedTile.click();
        }
    }
});

// Initialize tiles - make focusable and add effects
function initTiles() {
    tiles = document.querySelectorAll('.tile');
    character = document.getElementById('character');
    pathContainer = document.querySelector('.path-container');

    if (!tiles || tiles.length === 0) return;

    // Make tiles focusable
    tiles.forEach(tile => {
        tile.setAttribute('tabindex', '0');

        // Add number below tile
        const projectId = tile.dataset.project;
        const project = projects[projectId];
        if (project && project.projectNumber) {
            const numberEl = document.createElement('div');
            numberEl.className = 'tile-number';
            numberEl.textContent = String(project.projectNumber).padStart(2, '0');
            tile.appendChild(numberEl);
        }
    });

    // Add ripple effect on click
    tiles.forEach(tile => {
        tile.addEventListener('click', function (e) {
            const ripple = document.createElement('div');
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.6)';
            ripple.style.width = '96px';
            ripple.style.height = '96px';
            ripple.style.animation = 'ripple 0.6s ease-out';

            const rect = this.getBoundingClientRect();
            ripple.style.left = `${e.clientX - rect.left - 48}px`;
            ripple.style.top = `${e.clientY - rect.top - 48}px`;
            this.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        });
    });
}

// Add ripple animation
const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

console.log('Portfolio landing page loaded successfully!');
console.log('Click any tile to test - result will show "true"');

// Animate butterflies in random directions
function initButterflies() {
    const butterfly1 = document.querySelector('.butterfly-1');
    const butterfly2 = document.querySelector('.butterfly-2');

    if (!butterfly1 || !butterfly2) return;

    function randomFloat(min, max) {
        return Math.random() * (max - min) + min;
    }

    function moveButterfly(butterfly, duration) {
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        const rect = butterfly.getBoundingClientRect();
        const startX = rect.left;
        const startY = rect.top;

        const endX = randomFloat(50, viewportWidth - 50);
        const endY = randomFloat(50, viewportHeight - 50);

        const rotation = randomFloat(-180, 180);
        const distanceX = endX - startX;
        const distanceY = endY - startY;

        butterfly.style.transition = `left ${duration}ms ease-in-out, top ${duration}ms ease-in-out, transform ${duration}ms ease-in-out`;
        butterfly.style.left = `${endX}px`;
        butterfly.style.top = `${endY}px`;
        butterfly.style.transform = `translate(0, 0) rotate(${rotation}deg)`;

        setTimeout(() => {
            moveButterfly(butterfly, randomFloat(15000, 25000));
        }, duration);
    }

    // Start animations after page loads
    setTimeout(() => {
        moveButterfly(butterfly1, randomFloat(15000, 25000));
        moveButterfly(butterfly2, randomFloat(18000, 28000));
    }, 3000);
}

// Start butterfly animation after loading
window.addEventListener('load', () => {
    setTimeout(() => {
        initButterflies();
    }, 2500);
});

// Bottom Overlay Panel
const bottomOverlay = document.getElementById('bottomOverlay');
let isPanelExpanded = false;
let bottomScrollInterval = null;

// Auto-scroll bottom panel content
function autoScrollBottomPanel() {
    if (!bottomOverlay) return;

    // Reset scroll position
    bottomOverlay.scrollTop = 0;

    // Clear any existing interval
    if (bottomScrollInterval) {
        clearInterval(bottomScrollInterval);
        bottomScrollInterval = null;
    }

    const scrollDuration = 10000; // 10 seconds, same as tile panels
    const scrollHeight = bottomOverlay.scrollHeight - bottomOverlay.clientHeight;

    const scrollStep = scrollHeight > 0 ? (scrollHeight / (scrollDuration / 16)) : 0; // 60fps
    let currentScroll = 0;

    bottomScrollInterval = setInterval(() => {
        currentScroll += scrollStep;
        if (currentScroll >= scrollHeight) {
            bottomOverlay.scrollTop = scrollHeight;
            clearInterval(bottomScrollInterval);
            bottomScrollInterval = null;
        } else {
            bottomOverlay.scrollTop = currentScroll;
        }
    }, 16);
}

// Toggle panel expanded state
function togglePanel() {
    isPanelExpanded = !isPanelExpanded;
    bottomOverlay.classList.toggle('expanded', isPanelExpanded);

    // Prevent scrolling on body when panel is expanded
    document.body.style.overflow = isPanelExpanded ? 'hidden' : '';

    // Start or stop auto-scroll for bottom panel
    if (isPanelExpanded) {
        autoScrollBottomPanel();
    } else {
        if (bottomScrollInterval) {
            clearInterval(bottomScrollInterval);
            bottomScrollInterval = null;
        }
        bottomOverlay.scrollTop = 0;
    }
}

// Close panel when clicking outside
function closePanel(e) {
    if (isPanelExpanded && !bottomOverlay.contains(e.target)) {
        isPanelExpanded = false;
        bottomOverlay.classList.remove('expanded');
        document.body.style.overflow = '';
    }
}

// Initialize bottom panel behavior
function initBottomPanel() {
    // Toggle panel on click
    bottomOverlay.addEventListener('click', (e) => {
        // Toggle whenever any visible part of the bottom panel is clicked
        togglePanel();
    });

    // Close panel when clicking outside
    document.addEventListener('click', closePanel);

    // Prevent panel from closing when clicking inside it
    bottomOverlay.addEventListener('click', (e) => {
        e.stopPropagation();
    });
}

// Media Viewer Elements
const mediaImage = document.getElementById('mediaImage');
const mediaVideo = document.getElementById('mediaVideo');
const prevMediaBtn = document.getElementById('prevMedia');
const nextMediaBtn = document.getElementById('nextMedia');
const mediaCounter = document.getElementById('mediaCounter');
const projectTitle = document.getElementById('projectTitle');
const projectDescription = document.getElementById('projectDescription');
const mediaClose = document.getElementById('mediaClose');

let currentMediaIndex = 0;
let currentProjectMedia = [];

// Project data with media and details
const projectsData = {
    'simple-html': {
        title: 'Simple HTML Basics',
        description: 'A collection of fundamental HTML examples and exercises to build a strong foundation in web development.',
        media: [
            { type: 'image', src: 'media/project1/screenshot1.jpg' },
            { type: 'video', src: 'media/project1/demo.mp4' }
        ]
    },
    'todo-app': {
        title: 'To-Do App',
        description: 'A responsive task management application with add, complete, and delete functionality.',
        media: [
            { type: 'image', src: 'media/project2/screenshot1.jpg' },
            { type: 'video', src: 'media/project2/demo.mp4' }
        ]
    },
    'password-generator': {
        title: 'Password Generator',
        description: 'A secure password generator with customizable length and character options.',
        media: [
            { type: 'image', src: 'media/project3/screenshot1.jpg' },
            { type: 'video', src: 'media/project3/demo.mp4' }
        ]
    },
    '30-seconds': {
        title: '30 Seconds Game',
        description: 'A fast-paced game where you have 30 seconds to complete quick challenges.',
        media: [
            { type: 'image', src: 'media/project4/screenshot1.jpg' },
            { type: 'video', src: 'media/project4/demo.mp4' }
        ]
    },
    'swish-kunai': {
        title: 'Swish Kunai',
        description: 'A fast-paced ninja game with fluid movement and combat mechanics.',
        media: [
            { type: 'image', src: 'media/project5/screenshot1.jpg' },
            { type: 'video', src: 'media/project5/gameplay.mp4' }
        ]
    },
    'aves-derivative': {
        title: 'Aves Derivative',
        description: 'A project exploring advanced visualization techniques and data representation.',
        media: [
            { type: 'image', src: 'media/project6/screenshot1.jpg' },
            { type: 'video', src: 'media/project6/demo.mp4' }
        ]
    }
};

function openProject(projectId) {
    const project = projectsData[projectId];
    if (!project) return;

    // Update project details if elements exist
    if (projectTitle) projectTitle.textContent = project.title;
    if (projectDescription) projectDescription.textContent = project.description;

    // Set up media if available
    if (project.media) {
        currentProjectMedia = project.media;
        currentMediaIndex = 0;
        showCurrentMedia();
    }

    // Use panelManager instead of direct detailPanel access
    panelManager.open(projectId);
    isPanelOpen = true;
    currentOpenTileId = projectId;
}

function closeDetailPanel() {
    if (panelManager.currentOpenPanel) {
        panelManager.close(panelManager.currentOpenPanel);
        isPanelOpen = false;
        currentOpenTileId = null;
    }
}

function showCurrentMedia() {
    if (currentProjectMedia.length === 0) return;

    const media = currentProjectMedia[currentMediaIndex];

    // Check if media elements exist before using them
    if (mediaImage && mediaVideo) {
        // Hide both first
        mediaImage.style.display = 'none';
        mediaVideo.style.display = 'none';

        if (media.type === 'image') {
            mediaImage.src = media.src;
            mediaImage.style.display = 'block';
        } else if (media.type === 'video') {
            mediaVideo.src = media.src;
            mediaVideo.style.display = 'block';
            mediaVideo.play();
        }
    }

    // Update counter if it exists
    if (mediaCounter) {
        mediaCounter.textContent = `${currentMediaIndex + 1}/${currentProjectMedia.length}`;
    }

    // Update button states if they exist
    if (prevMediaBtn && nextMediaBtn) {
        prevMediaBtn.disabled = currentMediaIndex === 0;
        nextMediaBtn.disabled = currentMediaIndex === currentProjectMedia.length - 1;
    }
}

function showNextMedia() {
    if (currentMediaIndex < currentProjectMedia.length - 1) {
        currentMediaIndex++;
        showCurrentMedia();
    }
}

function showPrevMedia() {
    if (currentMediaIndex > 0) {
        currentMediaIndex--;
        showCurrentMedia();
    }
}

// Event Listeners for media viewer
if (mediaClose) mediaClose.addEventListener('click', closeDetailPanel);
if (prevMediaBtn) prevMediaBtn.addEventListener('click', showPrevMedia);
if (nextMediaBtn) nextMediaBtn.addEventListener('click', showNextMedia);

// Close when clicking on the media close button
if (mediaClose) {
    mediaClose.addEventListener('click', (e) => {
        e.stopPropagation();
        closeDetailPanel();
    });
}

// Close when clicking outside - handled by panelManager.init() already
// No need for separate detailPanel handler

// Keyboard navigation for panels
document.addEventListener('keydown', (e) => {
    // Only handle if a panel is open
    if (!isPanelOpen) return;

    switch (e.key) {
        case 'Escape':
            closeDetailPanel();
            break;
        case 'ArrowLeft':
            if (currentOpenTileId && currentOpenTileId !== 'simple-html') {
                showPrevMedia();
            }
            break;
        case 'ArrowRight':
            if (currentOpenTileId && currentOpenTileId !== 'simple-html') {
                showNextMedia();
            }
            break;
    }
});

// Function to log tile positions
function logTilePositions() {
    const tiles = document.querySelectorAll('.tile');
    console.clear();
    console.log('=== TILE POSITIONS ===');
    tiles.forEach((tile, index) => {
        const rect = tile.getBoundingClientRect();
        console.log(`Tile ${index + 1} (${tile.getAttribute('data-project') || 'no-data-project'})`);
        console.log({
            left: Math.round(rect.left) + 'px',
            top: Math.round(rect.top) + 'px',
            width: Math.round(rect.width) + 'px',
            height: Math.round(rect.height) + 'px'
        });
        console.log('-------------------');
    });
}

// Initialize when page loads
window.addEventListener('load', () => {
    // Show the panel with a slight delay
    setTimeout(() => {
        bottomOverlay.classList.add('open');
        initBottomPanel();

        // Click handlers are already set up in initTileHandlers() - no need to duplicate
        // Conversation clouds already initialized in DOMContentLoaded

        // Initialize media navigation
        if (prevMediaBtn) prevMediaBtn.addEventListener('click', showPrevMedia);
        if (nextMediaBtn) nextMediaBtn.addEventListener('click', showNextMedia);

        // Keyboard navigation is handled above in the main keydown listener
    }, 800);
});

// Typing animation function
function typeText(element, text, speed = 80) {
    if (!element) return;

    element.textContent = '';
    let index = 0;

    function type() {
        if (index < text.length) {
            element.textContent += text.charAt(index);
            index++;
            setTimeout(type, speed);
        } else {
            // Remove cursor after typing completes
            const cursor = document.querySelector('.typing-cursor');
            if (cursor) {
                setTimeout(() => {
                    cursor.style.opacity = '0';
                    setTimeout(() => cursor.remove(), 300);
                }, 500);
            }
        }
    }

    type();
}

// Fade in tiles one by one
function fadeInTiles() {
    const tiles = document.querySelectorAll('.tile');
    tiles.forEach((tile, index) => {
        setTimeout(() => {
            tile.classList.add('fade-in');
        }, index * 300); // 300ms delay between each tile (slower)
    });
}

// SIMPLE LOADER REMOVAL - This must work first!
function removeLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        document.body.classList.remove('loading');
        loader.classList.add('loader-hide');
        setTimeout(() => {
            if (loader.parentNode) {
                loader.remove();
            } else {
                loader.style.display = 'none';
            }
        }, 700);
    } else {
        // Fallback if loader element doesn't exist
        document.body.classList.remove('loading');
    }
}

// Fade out loader and reveal page - PRIORITY FUNCTION
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Starting loader removal');

    // Initialize DOM element references
    settingsBtn = document.getElementById('settingsBtn');
    settingsOverlay = document.getElementById('settingsOverlay');
    settingsThemeToggle = document.getElementById('settingsThemeToggle');
    playPauseBtn = document.getElementById('playPauseBtn');
    volumeSlider = document.getElementById('volumeSlider');
    volumeValue = document.getElementById('volumeValue');
    menuBtn = document.getElementById('menuBtn');
    menuOverlay = document.getElementById('menuOverlay');

    // Initialize all UI components
    try {
        initTiles(); // Must be first to set up tiles, character, pathContainer
        initCharacterMovement(); // Initialize character after tiles
        initSettings();
        initThemeToggle();
        initPlayPause();
        initVolumeSlider();
        initMenuOverlay();
        initTileHandlers();

        // Initialize conversation clouds after tiles are ready
        setTimeout(() => {
            initConversationClouds();
        }, 300);
    } catch (e) {
        console.error('Error initializing UI components:', e);
    }

    // Remove loader after short delay
    setTimeout(() => {
        console.log('Removing loader...');
        removeLoader();

        // Start typing animation after loader is removed
        setTimeout(() => {
            const typingText = document.getElementById('typingText');
            if (typingText && typeof typeText === 'function') {
                try {
                    typeText(typingText, 'Explore My Projects', 80);
                    // Start fading in tiles after typing starts
                    setTimeout(() => {
                        if (typeof fadeInTiles === 'function') {
                            try {
                                fadeInTiles();
                            } catch (e) {
                                console.error('Error fading in tiles:', e);
                            }
                        }
                    }, 1000);
                } catch (e) {
                    console.error('Error starting typing animation:', e);
                }
            }
        }, 900);
    }, 800);

    // Fallback: force remove loader after 3 seconds no matter what
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            console.log('Fallback: Force removing loader');
            loader.style.display = 'none';
            document.body.classList.remove('loading');
        }
    }, 3000);
});


// Run logTilePositions on window resize
window.addEventListener('resize', logTilePositions);

// Initialize panel manager and conversation clouds when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    try {
        panelManager.init();
    } catch (e) {
        console.error('Error initializing panel manager:', e);
    }
});

// Conversation clouds initialization removed - handled in DOMContentLoaded after tiles init

// ABSOLUTE FALLBACK: Remove loader no matter what after 2 seconds
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            console.log('Window load fallback: Removing loader');
            loader.style.display = 'none';
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
        }
        document.body.classList.remove('loading');
        // Force container to be visible
        const container = document.querySelector('.container');
        if (container) {
            container.style.opacity = '1';
        }
        const header = document.querySelector('.header');
        if (header) {
            header.style.opacity = '1';
            header.style.transform = 'translateY(0)';
        }
        const pathContainer = document.querySelector('.path-container');
        if (pathContainer) {
            pathContainer.style.opacity = '1';
            pathContainer.style.transform = 'translateY(0)';
        }
    }, 2000);
});
