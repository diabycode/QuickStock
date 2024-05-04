const loader = document.querySelector(".loader")
const clickables = document.querySelectorAll("button, a")

Array.from(clickables, (clickable) => {
    clickable.addEventListener("click", () => {
        loader.classList.remove("hide");
    })
})

window.addEventListener("load", () => {
    loader.classList.add("hide");
})


