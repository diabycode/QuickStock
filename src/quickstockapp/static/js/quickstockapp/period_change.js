document.querySelector("#period").addEventListener("change", (e) => {
    e.target.closest("form").submit()
    // document.querySelector("#submit_period").click();
})