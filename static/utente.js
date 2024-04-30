fetch("/api/user-info")
    .then(res => res.json())
    .then(user => {
        let btn = document.getElementById("btn_nome")
        btn.innerText = `${user.nome} ${user.cognome}`

    })

let theme = document.getElementById("theme")

let nuovo = localStorage.getItem("theme") != null ? localStorage.getItem("theme") : "retro"
theme.checked = nuovo == "retro" ? true : false
localStorage.setItem("theme", nuovo)

theme.addEventListener("click", (event) => {
    console.log("ok")
    let attuale = localStorage.getItem("theme")
    console.log(attuale)
    if (attuale == "retro")
        localStorage.setItem("theme", "sunset")
    else
        localStorage.setItem("theme", "retro")

    location.reload()
})

if (localStorage.getItem("theme") == "retro"){
    document.getElementById("spese").classList.add("text-base-100")
    document.getElementById("nome").classList.add("text-base-100")
}