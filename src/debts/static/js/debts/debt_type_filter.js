document.getElementById("id_debt_type").addEventListener("change", (e) => {
    e.target.closest("form").submit();
})