document.addEventListener('DOMContentLoaded', () => {
    titleLabel = document.getElementById("signup-form__title-label");
    titleInput = document.getElementById("id_title");
    studentRadioBtn = document.getElementById("id_role_0");
    instructorRadioBtn = document.getElementById("id_role_1");

    studentRadioBtn.addEventListener("click", () => {
        titleLabel.classList.add("hidden_element");
        titleInput.classList.add("hidden_element");
    })
    instructorRadioBtn.addEventListener("click", () => {
        titleLabel.classList.remove("hidden_element");
        titleInput.classList.remove("hidden_element");
    })

})