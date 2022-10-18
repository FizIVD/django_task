document.querySelector('#title').text = 'Изменение должности'
position_id = get_id()
get_position_data(position_id)

//Функция возвращат id должности из параметра адресной строки
function get_id() {
    const paramsString = document.location.search;
    const searchParams = new URLSearchParams(paramsString);
    return searchParams.get("id")
}

//Функция получает данные для заполнения полей должности, категории и id POST запросом
function get_position_data(id) {
    const payload = {id}
    fetch('http://127.0.0.1:8000/get_position/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            fill_fields(data)
        });

}

//Функция заполняет HTML шаблон данными текущей должности и категории
function fill_fields(data) {
    const position = document.querySelector('#position')
    position.value = data.position
    const category = document.querySelector('#category')
    category.value = data.category
    const id = document.querySelector('#ID')
    id.value = position_id
}

//Функция отправляет обновленные данные текущей должности и категории, в случае успеха обновляет таблицу должностей и закрывает окно.
//Отправляются данные только непустого поля "Должность", пустое поле игнорируется, запись не изменяется.
//Поле id только для чтения
//Если обновляемая запись не соотвтствует требованиям, выдается окно с указанием ошибки.
function update_position(id) {
    const position = document.querySelector('#position').value
    const category = document.querySelector('#category').value
    const payload = {id, position, category}
    for (let item in payload) {
        if (payload.hasOwnProperty(item) && (payload[item] === '' || payload[item] === ' ')) {
            delete payload[item]
        }
    }
    fetch('http://127.0.0.1:8000/update_position/', {
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

//Функция отправляет id удаляемой должности и категории, в случае успеха обновляет таблицу должностей и закрывает окно.
//В случае ошибки, выдается окно с указанием ошибки.
function delete_position(id) {
    const payload = {id}
    fetch('http://127.0.0.1:8000/del_position/', {
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