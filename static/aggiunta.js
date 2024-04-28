fetch("/api/user-info")
    .then(res => res.json())
    .then(user => {
        let btn = document.getElementById("nome")
        btn.innerText = `${user.nome} ${user.cognome}`
    })


fetch("/api/tipologie")
    .then(res => res.json())
    .then(data => {
        let selectTipologia = document.getElementById("tipologia")
        data.forEach(tipologia => {
            let opt = document.createElement("option")
            opt.value = tipologia.id
            opt.innerText = tipologia.descrizione
            selectTipologia.appendChild(opt)
        })
    })

let theme = document.getElementById("theme")
console.log(theme)
const attuale = theme.getAttribute("data-theme");
console.log(attuale)

let nuovo = localStorage.getItem("theme") != null ? localStorage.getItem("theme") : "retro"
theme.setAttribute("data-theme", nuovo == "retro" ? "retro" : "sunset")
localStorage.setItem("theme", nuovo)

if (localStorage.getItem("theme") == "retro"){
    document.getElementById("spese").classList.add("text-base-100")
    document.getElementById("nome").classList.add("text-base-100")
}