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