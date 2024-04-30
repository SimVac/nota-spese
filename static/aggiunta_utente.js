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
