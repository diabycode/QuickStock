
// const pinCodeInput = document.getElementById("id_pin_code")
// // pinCodeInput.classList.add("hide")

// const passwordConfirm = document.querySelector(".password-confirm")
// // passwordConfirm.classList.add("hide")

// const pincodeFormContent = document.getElementById("pin-code-form-content")
// pincodeFormContent.classList.add("hide")

// const pinCodeContainer = pinCodeInput.closest("div.pin-code")
// const p = document.createElement("p")
// const editBtn = document.createElement("a")
// editBtn.innerText = "modifier"
// editBtn.classList.add("pin-edit-btn")
// editBtn.setAttribute("href", "#")
// const span = document.createElement("span")
// span.innerText = "****"
// span.classList.add("pin-code-hashed")
// p.appendChild(span)
// p.appendChild(editBtn)
// pinCodeContainer.appendChild(p)

// editBtn.addEventListener("click", (e) => {
//     e.preventDefault();
//     pincodeFormContent.classList.remove("hide")
//     p.classList.add("hide")
// })

// function formSubmit(e) {
//     e.preventDefault()
//     const formdata = new FormData(e.target)
    
//     if (formdata.get("pin_code") && !formdata.get("password")) {
//         document.querySelector(".password-confirm").classList.add("error");
//     } else if (!formdata.get("pin_code") && formdata.get("password")) {
//         document.querySelector("#id_pin_code").classList.add("error")
//     } else e.target.submit()
// }
// const form = document.querySelector(".settings-form")
// form.addEventListener("submit", formSubmit)






