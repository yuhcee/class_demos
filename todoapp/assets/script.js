const descInput = document.getElementById('description');
document.getElementById('form').onsubmit = function (e) {
    e.preventDefault();
    const desc = descInput.value;

    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({ description: desc }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            const liItem = document.createElement('li');
            liItem.innerHTML = jsonResponse['description'];
            document.getElementById('todos').appendChild(liItem);
            document.getElementById('error').classname = 'hidden';
        })
        .catch(function () {
            document.getElementById('error').className = '';
        });
};
