document.addEventListener('DOMContentLoaded', () => {
    let allCards = document.querySelectorAll(".course-card__card-anchor");
    let slicedArrayCards = [...allCards].slice(2); //select from the second element to the end
    const showLessCoursesBtn = document.getElementById("show-less-courses");
    const showMoreCoursesBtn = document.getElementById("show-all-courses");

    // When DOM content loads
    showLessCoursesBtn.style.display = "none";

    slicedArrayCards.forEach(card => {
        card.style.display = "none";
    })

    // Event listeners
    showMoreCoursesBtn.addEventListener("click", () => {
        showMoreCoursesBtn.style.display = "none";
        showLessCoursesBtn.style.display = "inline-block";
        slicedArrayCards.forEach(card => {
            card.style.display = "inline";
        })
    })

    showLessCoursesBtn.addEventListener("click", () => {
        showLessCoursesBtn.style.display = "none";
        showMoreCoursesBtn.style.display = "inline-block";
        slicedArrayCards.forEach(card => {
            card.style.display = "none";
        })
    })
})
