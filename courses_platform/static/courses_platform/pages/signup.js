document.addEventListener('DOMContentLoaded', () => {
    titleLabel = document.getElementById("signup-form__title-label");
    titleInput = document.getElementById("id_title");

    if (titleInput.classList.contains("hidden-element")) {
        titleLabel.classList.add("hidden-element");
    }

    studentRadioBtn = document.getElementById("id_role_0");
    instructorRadioBtn = document.getElementById("id_role_1");

    studentRadioBtn.addEventListener("click", () => {
        titleLabel.classList.add("hidden-element");
        titleInput.classList.add("hidden-element");
    })
    instructorRadioBtn.addEventListener("click", () => {
        titleLabel.classList.remove("hidden-element");
        titleInput.classList.remove("hidden-element");
    })

    //Remove red border of input field when starting to write in it
    redBorderInputs = document.querySelectorAll(".signup-form__input-red-border");

    function removeRedBorder(event) {
        event.target.classList.remove("signup-form__input-red-border");
        event.target.removeEventListener("input", removeRedBorder);
    }

    redBorderInputs.forEach(inputField => {
        inputField.addEventListener("input", removeRedBorder);
    })

})