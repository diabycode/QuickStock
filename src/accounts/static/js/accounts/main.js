// search errors on page loaded
window.addEventListener("load", () => {
    const errors = document.querySelectorAll(".error")
    if (errors.length > 0) {
        errors.forEach((error) => {
            error.closest("div").parentElement.querySelector("input").classList.add("error-input")
        })
    }
})


// test password confirmation
const password = document.querySelector("#id_password")
document.querySelector("input[name=password-repeat").addEventListener("input", (e) => {
    if (e.target.value !== password.value) {
        if (e.target.classList.contains("error-input")) {return}
        e.target.classList.add("error-input")
    } else {
        e.target.classList.remove("error-input")
    }
})


