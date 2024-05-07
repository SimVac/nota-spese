fetch('api/roles')
    .then(response => response.json())
    .then(data => {
        data.forEach(role => {
            const option = document.createElement('option');
            option.value = role.id;
            option.textContent = role.nome;
            document.getElementById('ruolo').appendChild(option);
        });
    })
    .catch(error => {
        console.error('Error fetching roles:', error);
    });

    fetch("api/user-info")
    .then(res => res.json())
    .then(user => {
        let btn = document.getElementById("nome")
        btn.innerText = `${user.nome} ${user.cognome}`
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
    document.getElementById("btn_nome").classList.add("text-base-100")
}