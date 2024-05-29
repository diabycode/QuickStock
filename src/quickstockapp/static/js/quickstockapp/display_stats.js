function displayStats () {
    const response = fetch("/display_stats/", {method: "GET",})
    .then(rp => rp.json())
    .then(rp => {
        if (rp.success) location.reload();
    })
}
document.addEventListener("DOMContentLoaded", () => {
    const displayBtn = document.querySelector(".stats-display-btn");
    if (!displayBtn.classList.contains("protected-action")) {
        displayBtn.addEventListener("click", displayStats)
    }
})