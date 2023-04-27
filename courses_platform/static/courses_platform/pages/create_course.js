document.addEventListener('DOMContentLoaded', () => {
    let temp = document.getElementsByTagName("template")[0];
    let quiz = temp.content.cloneNode(true);
    document.getElementById("quiz-container").appendChild(quiz);

    let addQuestionBtn = document.getElementById("add-question-btn");
    addQuestionBtn.addEventListener("click", () => {
        let temp = document.getElementsByTagName("template")[0];
        let quiz = temp.content.cloneNode(true);
        document.getElementById("quiz-container").appendChild(quiz);
    })
})