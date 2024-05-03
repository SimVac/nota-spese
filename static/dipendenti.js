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
