document.querySelector('#title').text = 'Новая должность'

//Функция отправляет данные новой должности и категории, в случае успеха обновляет таблицу должностей и закрывает окно.
//Отправляются данные только непустого поля "Должность", пустое поле игнорируется, выводится ошибка.
//Если новая запись не соотвтствует требованиям, выдается окно с указанием ошибки.
function create_position() {
    const position = document.querySelector('#position').value
    const category = document.querySelector('#category').value
    const payload = {position, category}
    for (let item in payload) {
        if (payload.hasOwnProperty(item) && (payload[item] === '' || payload[item] === ' ')) {
            delete payload[item]
        }
    }
    fetch('http://127.0.0.1:8000/create_position/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(payload)
    }).then(response => response.json())
        .then(data => {
            data.error ? window.alert(data.error) : (opener.location.reload(), window.close())
        })
}