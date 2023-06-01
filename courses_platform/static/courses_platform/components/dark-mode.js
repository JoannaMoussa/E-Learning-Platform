document.addEventListener('DOMContentLoaded', () => {
    const sunIcons = document.querySelectorAll("#theme-toggle-sun");
    const moonIcons = document.querySelectorAll("#theme-toggle-moon");
    const themeToggleBtns = document.querySelectorAll("#theme-toggle");
    
    // hide the sun icon from nav bar and from mobile menu
    sunIcons.forEach(icon => {
        icon.style.display = "none";
    })

    // In the 2 lines of code below, we are specifying what the theme will be on mount 
    // (=on first page visit and on page reload), 
    // based on what the user chose last time he was on the website

    // getItem takes a string argument that is the name of the key in the local storage,
    // and returns the value of that key, or returns null if the key is not found.
    const theme = localStorage.getItem("theme");
    // The line below means that if the theme variable is not null, the code after "&&" will be executed
    // Given that the below line of code isn't inside a statement, 
    // it runs the moment the page is loaded. (this is called on mount)

    // on mount
    theme && document.body.classList.add(theme);

    // Events 
    themeToggleBtns.forEach(btn =>
        btn.addEventListener("click", () => {
            // change the theme toggle icon
            const sunIcon = document.getElementById("theme-toggle-sun");
            if (sunIcon.style.display == "none") {
                sunIcons.forEach(icon => {
                    icon.style.display = "block";
                })
                moonIcons.forEach(icon => {
                    icon.style.display = "none";
                })
            }
            else {
                sunIcons.forEach(icon => {
                    icon.style.display = "none";
                })
                moonIcons.forEach(icon => {
                    icon.style.display = "block";
                })
            }

            // Give the class dark-mode to the body or remove it and update the local storage accordingly
            document.body.classList.toggle("dark-mode");
            if (document.body.classList.contains("dark-mode")) {
                // The setItem() will create a key value pair inside our local storage
                // it takes 2 string arguments: the name of the key and the name of the value.
                localStorage.setItem("theme", "dark-mode");
            }
            else {
                // removeItem() takes one string argument: the key we want to remove from our local storage
                localStorage.removeItem("theme");
                // In order to avoid the body having an empty class attribute, we can remove it.
                document.body.removeAttribute("class");
            }
        })
    );

});



