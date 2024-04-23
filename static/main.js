const table = document.getElementById("tabellaSpese")

fetch("/api/user-notes")
    .then(res => res.json())
    .then(data => {
        data.forEach((nota, idx) => {
            const tr = document.createElement("tr")
            let td = document.createElement("td")
            td.innerText = idx + 1
            tr.appendChild(td)
            td = document.createElement("td")
            td.innerText = "Nome"
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