// Loader animation - hide after page loads
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    setTimeout(() => {
        loader.classList.add('loader-hide');
        document.body.classList.remove('loading');
        setTimeout(() => {
            loader.style.display = 'none';
        }, 600);
    }, 1500); // Show loader for 1.5 seconds
});
