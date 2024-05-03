


// Array.from(options).forEach(element => {
//     let code = element.getAttribute("value");
//     element.appendChild(span)
// })

const select = document.querySelector("#id_accent_color_code")
const elementToInsertAfter = document.querySelector("label[for=id_accent_color_code]")
let span = document.createElement("span")
span.classList.add("theme-ilustration")
// span.style.backgroundColor = code
elementToInsertAfter.insertAdjacentElement("beforeend", span)

span.style.backgroundColor = select.value;

select.addEventListener("change", (e) => {
    span.style.backgroundColor = select.value;
})



