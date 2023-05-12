document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById("success") !== null) {
        startConfetti();
        setTimeout(stopConfetti, 5000)
    }
})
