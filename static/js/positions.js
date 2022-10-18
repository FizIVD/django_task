document.querySelector('#title').text = 'Должности'
request_position_data()

//Функция получает список должностей и категорий GET запросом
function request_position_data() {
    fetch('http://127.0.0.1:8000/positions/')
        .then(response => response.json())
        .then(data => {
            render_table(data);
        });
}

//Функция создает таблицу должностей и категорий без id
function render_table(table_data) {
    let table = document.querySelector('#staff');
    let rowHeader = table.insertRow();
    for (let prop in table_data[0]) {
        if (prop !== 'id') {
            let cell = rowHeader.insertCell();
            cell.innerText = prop;
        }
    }
    for (let i = 0; i < table_data.length; i++) {
        let row = table.insertRow();
        for (let prop in table_data[i]) {
            if (prop !== 'id') {
                let cell = row.insertCell();
                if (prop === 'position') {
                    cell.innerHTML = `<p style="color: darkblue; font-weight: bolder" onclick="window.open('/app/edit_position/?id=${table_data[i]['id']}', 'Изменение должности', 'width=1000,height=400');">` + table_data[i][prop] + "</p>";
                } else {
                    cell.innerText = table_data[i][prop];
                }
            }
        }
    }
}