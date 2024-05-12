
const statsDisplayForm = document.getElementById("stats_display")
statsDisplayForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (statsDisplayForm.classList.contains("hide")) {
        const pinTestModal = document.querySelector(".pin-code-test")
        pinTestModal.classList.remove("hide");
        document.body.addEventListener("click", e => {
            e.stopPropagation();
            if (!e.target.closest(".pin-code-test")) pinTestModal.classList.add("hide")
        })     
    } else e.target.submit()
})

