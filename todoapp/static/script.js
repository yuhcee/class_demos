const descInput = document.getElementById('description');
const checkboxes = document.querySelectorAll('.check-completed');
const deleteBtns = document.querySelectorAll('.delete-button');

for (let i = 0; i < deleteBtns.length; i++) {
    const deleteBtn = deleteBtns[i];
    deleteBtn.onclick = function (e) {
        const todoId = e.target.dataset['id'];
        fetch('/todos/' + todoId, {
            method: 'DELETE',
        }).then(function () {
            const item = e.target.parentElement;
            item.remove;
            location.reload();
        });
    };
}

for (let i = 0; i < checkboxes.length; i++) {
    const checkbox = checkboxes[i];
    checkbox.onchange = function (e) {
        const completed = e.target.checked;
        const todoId = e.target.dataset['id'];
        fetch('/todos/' + todoId + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({ completed }),
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(function () {
                document.getElementById('error').className = 'hidden';
            })
            .catch(function () {
                document.getElementById('error').className = '';
            });
    };
}

document.getElementById('form').onsubmit = function (e) {
    e.preventDefault();
    const description = descInput.value;

    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({ description }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (jsonResponse) {
            const li = document.createElement('li');
            const checkbox = document.createElement('input');
            checkbox.className = 'check-completed';
            checkbox.type = 'checkbox';
            checkbox.setAttribute('data-id', jsonResponse.id);
            li.appendChild(checkbox);

            const text = document.createTextNode(' ' + jsonResponse.description);
            li.appendChild(text);

            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-button';
            deleteBtn.setAttribute('data-id', jsonResponse.id);
            deleteBtn.innerHTML = '&cross;';
            li.appendChild(deleteBtn);

            document.getElementById('todos').appendChild(li);
            document.getElementById('error').classname = 'hidden';
            location.reload();
        })
        .catch(function (e) {
            console.log(e);
            console.error('Error occured');
            document.getElementById('error').className = '';
        });
};
