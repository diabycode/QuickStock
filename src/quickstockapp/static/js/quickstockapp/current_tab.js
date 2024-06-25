const currentTab = document.getElementById("current_tab")
if (currentTab) {
    const menu = Array.from(document.querySelectorAll(".sidebar-content .menu li"))
    menu.forEach(li => {
        const a = li.querySelector("a");
        if (a.href.includes(currentTab.value)) li.classList.add("current");  
        else if (a.href.includes(currentTab.value)) li.classList.add("current");  
        else if (a.href.includes(currentTab.value)) li.classList.add("current");  
        else if (a.href.includes(currentTab.value)) li.classList.add("current");  
    })
}