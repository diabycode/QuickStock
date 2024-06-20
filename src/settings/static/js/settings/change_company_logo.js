const imgField = document.getElementById("id_company_logo")
const preview = document.getElementById("logo_preview");
function previewImage(event) {
    preview.style.display = "";
    let reader = new FileReader();
    reader.onload = function() {
        preview.src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
    preview.style.opacity = ".4"
}; imgField.addEventListener("change", previewImage);


// const clearImage = document.getElementById("company_logo-clear_id")
// clearImage.addEventListener("change", (event) => {
//     if (event.target.checked) preview.style.opacity = ".4"
//     else preview.style.opacity = "1"
// }); 

// const changeLogo = document.getElementById("change_logo_fields")

document.getElementById("company_logo_fields").style.display = "none";