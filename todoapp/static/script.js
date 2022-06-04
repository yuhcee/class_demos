const listId = document.getElementById('list_id');
const descInput = document.getElementById('description');
const deleteBtns = document.querySelectorAll('.delete-todo');
const deleteListBtns = document.querySelectorAll(".delete-list");
const todoCheckboxes = document.querySelectorAll('.todo-check-completed');
const listCheckboxes = document.querySelectorAll('.list-check-completed');

for (let i = 0; i < deleteBtns.length; i++) {
    const deleteBtn = deleteBtns[i];
    deleteBtn.onclick = function (e) {
        const todoId = e.target.dataset['id'];
        fetch('/todos/' + todoId + '/delete', {
            method: 'DELETE',
        })
            .then(function () {
                const item = e.target.parentElement;
                item.remove;
                document.getElementById('error').className = 'hidden';
                location.reload();
            })
            .catch(function (e) {
                console.error(e);
                document.getElementById('error').className = '';
            });
    };
}

for (let i = 0; i < todoCheckboxes.length; i++) {
    const checkbox = todoCheckboxes[i];
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

document.getElementById('todo-form').onsubmit = function (e) {
    e.preventDefault();
    const description = descInput.value;
    const list_id = listId.value;
    descInput.value = '';

    fetch('/todos/create', {
        method: 'POST',
        body: JSON.stringify({ description, list_id }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((jsonResponse) => {
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
        })
        .catch(function (e) {
            console.log(e);
            console.error('Error occured');
            document.getElementById('error').className = '';
        });
};

// ============================== LISTS ================================

for (let i = 0; i < listCheckboxes.length; i++) {
    const checkbox = listCheckboxes[i];

    checkbox.onchange = function (e) {
        if (e.target.checked) {
            const listId = e.target.dataset.id;

            fetch('/lists/' + listId + '/set-completed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then(function (jsonResponse) {
                    document.getElementById('error').className = 'hidden';

                    const todoCheckboxes = document.querySelectorAll('.todo-check-completed');

                    for (let i = 0; i < todoCheckboxes.length; i++) {
                        const checkbox = todoCheckboxes[i];

                        checkbox.checked = true;
                    }
                })
                .catch(function () {
                    document.getElementById('error').className = '';
                });
        }
    };
}
