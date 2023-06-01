document.addEventListener('DOMContentLoaded', () => {
    const headerBars = document.getElementById("header-bars");
    const CloseBtn = document.getElementById("mobile-nav-close-btn");
    const mobileNav = document.getElementById("mobile-navigation");
    const mobileNavLinks = document.querySelectorAll(".mobile-nav__link");

    headerBars.addEventListener("click", () => {
        mobileNav.style.display = "flex";
        document.body.style.overflowY = "hidden";
    })
    CloseBtn.addEventListener("click", () => {
        mobileNav.style.display = "none";
        document.body.style.overflowY = "auto";
    })
    mobileNavLinks.forEach(link => {
        link.addEventListener("click", () => {
            mobileNav.style.display = "none";
            document.body.style.overflowY = 'auto';
        })
    })
})



