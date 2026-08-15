// Lightweight login interactions (no remember me)
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('.login-form');
    const loginBtn = document.querySelector('.login-btn');

    if (loginForm && loginBtn) {
        loginForm.addEventListener('submit', function() {
            // Show simple loading state
            loginBtn.disabled = true;
            loginBtn.textContent = 'Iniciando...';
        });
    }

    // Gentle entrance for the login card (non-blocking)
    const loginCard = document.querySelector('.login-card');
    if (loginCard) {
        loginCard.style.opacity = 0;
        loginCard.style.transform = 'translateY(10px)';
        setTimeout(() => {
            loginCard.style.transition = 'all 360ms ease-out';
            loginCard.style.opacity = 1;
            loginCard.style.transform = 'translateY(0)';
        }, 80);
    }
});
