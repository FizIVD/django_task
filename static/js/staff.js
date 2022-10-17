request_staff_data()

//Функция получает список персонала GET запросом
function request_staff_data() {
    fetch('staff/')
        .then(response => response.json())
        .then(data => {
            render_table(data);
        });
}

//Функция создает таблицу списка персонала без id
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
                if (prop === 'full_name') {
                    cell.innerHTML = `<p style="color: darkblue; font-weight: bolder" onclick="window.open('/app/edit_employee/?id=${table_data[i]['id']}', 'Личная карточка сотрудника', 'width=1200,height=400');">` + table_data[i][prop] + "</p>";
                } else {
                    cell.innerText = table_data[i][prop];
                }
            }
        }
    }
}