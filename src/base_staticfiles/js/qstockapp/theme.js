const rootElement = document.querySelector(":root")
// const style = getComputedStyle(rootElement)

rootElement.style.setProperty("--primary", document.querySelector(".theme_color").innerText)