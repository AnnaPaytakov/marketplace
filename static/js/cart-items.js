document.addEventListener('DOMContentLoaded', function () {  // Ждём загрузки DOM
    const addBtns = document.querySelectorAll('.add-btn');  // Находим все кнопки добавления
    const subtractBtns = document.querySelectorAll('.subtract-btn');  // Находим все кнопки уменьшения
    const removeBtns = document.querySelectorAll('.remove-btn');  // Находим все кнопки удаления
    const buyBtn = document.getElementById('buy-btn');  // Находим кнопку покупки

    addBtns.forEach(btn => {  // Для каждой кнопки добавления
        btn.addEventListener('click', function () {  // Добавляем обработчик события клика
            const productId = this.getAttribute('data-id');  // Получаем ID продукта из атрибута
            updateCart('add', productId);  // Обновляем корзину с действием 'add'
        });
    });

    subtractBtns.forEach(btn => {  // Для каждой кнопки уменьшения
        btn.addEventListener('click', function () {  // Добавляем обработчик события клика
            const productId = this.getAttribute('data-id');  // Получаем ID продукта из атрибута
            updateCart('subtract', productId);  // Обновляем корзину с действием 'subtract'
        });
    });

    removeBtns.forEach(btn => {  // Для каждой кнопки удаления
        btn.addEventListener('click', function () {  // Добавляем обработчик события клика
            const productId = this.getAttribute('data-id');  // Получаем ID продукта из атрибута
            updateCart('remove', productId);  // Обновляем корзину с действием 'remove'
        });
    });

    function updateCart(action, productId) {  // Функция для обновления корзины
        let url = '';  // Инициализируем переменную URL

        if (action === 'add') {  // Если действие 'add'
            url = '/add-to-cart/';  // Устанавливаем URL для добавления
        } else if (action === 'subtract') {  // Если действие 'subtract'
            url = '/subtract-from-cart/';  // Устанавливаем URL для уменьшения
        } else if (action === 'remove') {  // Если действие 'remove'
            url = '/remove-from-cart/';  // Устанавливаем URL для удаления
        }

        fetch(url, {  // Выполняем запрос
            method: 'POST',  // Метод запроса POST
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),  // Добавляем CSRF токен
                'Content-Type': 'application/json',  // Устанавливаем тип содержимого JSON
            },
            body: JSON.stringify({ product_id: productId }),  // Передаём ID продукта в теле запроса
        })
        .then(response => response.json())  // Преобразуем ответ в JSON
        .then(data => {  // Обрабатываем данные
            if (data.status === 'success') {  // Если статус успешный
                window.location.reload();  // Перезагружаем страницу для обновления корзины
            } else {  // В противном случае
                alert(data.message);  // Показываем сообщение об ошибке
            }
        });
    }

    function getCookie(name) {  // Функция для получения значения куки
        let cookieValue = null;  // Инициализируем значение куки
        if (document.cookie && document.cookie !== '') {  // Если куки существуют
            const cookies = document.cookie.split(';');  // Разбиваем куки на массив
            for (let i = 0; i < cookies.length; i++) {  // Перебираем куки
                const cookie = cookies[i].trim();  // Удаляем пробелы по краям
                if (cookie.substring(0, name.length + 1) === (name + '=')) {  // Если куки совпадают с именем
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));  // Декодируем значение куки
                    break;  // Выходим из цикла
                }
            }
        }
        return cookieValue;  // Возвращаем значение куки
    }
});
