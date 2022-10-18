request_positions_data()
employee_id = get_id()
document.querySelector('#title').text = 'Личная карточка сотрудника'
document.querySelector('#label').innerHTML = 'Карточка сотрудника' + ' id: ' + employee_id
get_employee_data(employee_id)

//Функция возвращат id сотрудника из параметра адресной строки
function get_id() {
    const paramsString = document.location.search;
    const searchParams = new URLSearchParams(paramsString);
    return searchParams.get("id")
}

//Функция получает данные для заполнения полей формы POST запросом
function get_employee_data(id) {
    const payload = {id}
    console.log(payload)
    fetch('http://127.0.0.1:8000/get_employee/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            console.log(data)
            fill_fields(data)
        });

}

//Функция заполняет HTML шаблон данными текущего сотрудника (Фамилия, Имя, Отчество, возраст, пол, должность)
function fill_fields(data) {
    const second_name = document.querySelector('#second_name')
    second_name.value = data.full_name.split(' ')[0]
    const first_name = document.querySelector('#first_name')
    first_name.value = data.full_name.split(' ')[1]
    const father_name = document.querySelector('#father_name')
    father_name.value = data.full_name.split(' ')[2]
    const age = document.querySelector('#age')
    age.value = data.age
    const gender = document.querySelector('#select_gender')
    gender.value = data.gender
    const position = document.querySelector('#select_position')
    position.value = data.position

}

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

//Функция отправляет обновленные данные текущего сотрудника, в случае успеха обновляет таблицу сотрудников и закрывает окно.
//Отправляются данные только непустых полей, пустые поля игнорируется.
//Если обновляемая запись не соотвтствует требованиям, выдается окно с указанием ошибки.
function update_employee(id) {
    const full_name = document.querySelector('#second_name').value + ' ' + document.querySelector('#first_name').value + ' ' + document.querySelector('#father_name').value
    const gender = document.querySelector('#select_gender').value
    const age = +document.querySelector('#age').value
    const position = +document.querySelector('#select_position').value
    const payload = {id, full_name, gender, age, position}
    for (let item in payload) {
        if (payload.hasOwnProperty(item) && (payload[item] === '' || payload[item] === '  ' || payload[item] === 0)) {
            delete payload[item]
        }
    }
    fetch('http://127.0.0.1:8000/update_employee/', {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            data.error ? window.alert(data.error) : (opener.location.reload(), window.close());
        });

}
//Функция отправляет id удаляемого сотрудника, в случае успеха обновляет таблицу сотрудников и закрывает окно.
//В случае ошибки, выдается окно с указанием ошибки.
function delete_employee(id) {
    const payload = {id}
    fetch('http://127.0.0.1:8000/del_employee/', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            data.error ? window.alert(data.error) : (opener.location.reload(), window.close());
        });

}