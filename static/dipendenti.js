fetch("/api/users")
  .then((response) => response.json())
  .then((data) => {
    const table = document.getElementById("tabellaSpese");
    data.forEach((user, idx) => {
      const row = table.insertRow();
      const cell1 = row.insertCell(0);
      cell1.innerHTML = idx+1;
      const cell2 = row.insertCell(1);
      cell2.innerHTML = user.nome;
      const cell3 = row.insertCell(2);
      cell3.innerHTML = user.cognome;
      const cell4 = row.insertCell(3);
      cell4.innerHTML = user.username;
      const cell5 = row.insertCell(4);
      cell5.innerHTML = user.dataAssunzione;
      const cell6 = row.insertCell(5);
      cell6.innerHTML = user.ruolo;
    });
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
    }