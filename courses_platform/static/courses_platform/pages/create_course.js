document.addEventListener('DOMContentLoaded', () => {
    // Add event listener to "add question" btn
    let addQuestionBtn = document.getElementById("add-question-btn");
    addQuestionBtn.addEventListener("click", () => {
        let temp = document.getElementsByTagName("template")[0];
        let quiz = temp.content.cloneNode(true);

        // add event listener to "delete question" btn
        let quizDeleteBtn = quiz.getElementById("quiz-quest-del-btn");
        quizDeleteBtn.addEventListener("click", () => {
            quizDeleteBtn.parentElement.remove();
        })

        document.getElementById("quiz-container").appendChild(quiz); 
    })

    // If we're re-rendering the page after an error after publishing the course, 
    // in that case all the questions will be re-rendered in a new html page,
    // we should select all "delete question" btns and add event listeners on them 
    let allDeleteQuestionBtns = document.querySelectorAll("#quiz-quest-del-btn");
    allDeleteQuestionBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            btn.parentElement.remove();
        })
    })
})
