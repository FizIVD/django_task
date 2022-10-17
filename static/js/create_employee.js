document.querySelector('#title').text = 'Добавление сотрудника'
request_positions_data()

//Функция заполняет HTML шаблон выпадающего списка с выбором должности
function select_positions_fill(data) {
    const select_position = document.querySelector('#select_position')
    for (let row in data) {
        select_position.options[select_position.options.length] = new Option(data[row].position, data[row].id);
    }
}

//Функция получает данные для заполнения HTML шаблона выпадающего списка с выбором должности
function request_positions_data() {
    fetch('http://127.0.0.1:8000/positions/')
        .then(response => response.json())
        .then(data => {
            select_positions_fill(data)
        });
}

//Функция отправляет данные нового сотрудника, в случае успеха обновляет таблицу сотрудников и закрывает окно.
//Отправляются данные только непустых полей, пустые поля игнорируются, выводится ошибка.
//Если новая запись не соотвтствует требованиям, выдается окно с указанием ошибки.
function create_employee() {
    const full_name = document.querySelector('#second_name').value + ' ' + document.querySelector('#first_name').value + ' ' + document.querySelector('#father_name').value
    const gender = document.querySelector('#select_gender').value
    const age = +document.querySelector('#age').value
    const position = +document.querySelector('#select_position').value
    const payload = {full_name, gender, age, position}
    for (let item in payload) {
        if (payload.hasOwnProperty(item) && (payload[item] === '' || payload[item] === '  ' || payload[item] === 0)) {
            delete payload[item]
        }
    }

    fetch('http://127.0.0.1:8000/create_employee/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            data.error ? window.alert(data.error) : (opener.location.reload(), window.close())
        });
}