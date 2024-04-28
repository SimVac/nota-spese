let theme = document.getElementById("theme")
console.log(theme)
const attuale = theme.getAttribute("data-theme");
console.log(attuale)

let nuovo = localStorage.getItem("theme") != null ? localStorage.getItem("theme") : "retro"
theme.setAttribute("data-theme", nuovo == "retro" ? "retro" : "sunset")
localStorage.setItem("theme", nuovo)