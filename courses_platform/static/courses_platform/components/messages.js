document.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll("#single-message");
    const messageCloseBtns = document.querySelectorAll("#message-close-btn");

    messages.forEach(message => {
        message.addEventListener("animationend", () => {
            message.remove();
        })
    })
    
    messageCloseBtns.forEach(messageCloseBtn => {
        messageCloseBtn.addEventListener("click", (event) => {
            event.target.parentElement.remove();
        })
    })
})
