const table = document.getElementById("tabellaSpese")
var url = new URL(document.location.href);
let page = url.searchParams.get("page") || 1

fetch(`/api/user-notes/${page}`)
    .then(res => res.json())
    .then(data => {
        data.forEach((nota, idx) => {
            const tr = document.createElement("tr")
            let td = document.createElement("td")
            td.innerText = (page-1) * 10 + idx + 1
            tr.appendChild(td)
            td = document.createElement("td")
            td.innerText = nota.data
            tr.appendChild(td)
            td = document.createElement("td")
            td.innerText = nota.tipologia
            tr.appendChild(td)
            td = document.createElement("td")
            td.innerText = nota.importo
            tr.appendChild(td)
            td = document.createElement("td")
            td.innerText = "Allegati"
            tr.appendChild(td)
            table.appendChild(tr)
        });
    })
    .catch(err => console.error(err))


fetch("api/user-info")
    .then(res => res.json())
    .then(user => {
        let btn = document.getElementById("nome")
        btn.innerText = `${user.nome} ${user.cognome}`
    })