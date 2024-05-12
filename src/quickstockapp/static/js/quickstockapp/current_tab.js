const currentTab = document.getElementById("current_tab")
if (currentTab) {
    const menu = Array.from(document.querySelectorAll(".sidebar-content .menu li"))
    if (currentTab.value == "dashbord") menu[0].classList.add("current");  
    if (currentTab.value == "products") menu[1].classList.add("current");
    if (currentTab.value == "orders") menu[2].classList.add("current");
    if (currentTab.value == "sales") menu[3].classList.add("current");
}