function setUserType(userType, button) {
    // Убираем активный класс у всех кнопок
    const buttons = document.querySelectorAll('.d-flex button');
    buttons.forEach(function(btn) {
        btn.classList.remove('btn-success');
        btn.classList.add('btn-secondary');
    });

    // Добавляем активный класс на нажатую кнопку
    button.classList.add('btn-success');
    button.classList.remove('btn-secondary');

    // Устанавливаем значение скрытого поля в форму
    document.querySelector('input[name="user_type"]').value = userType;
    console.log(document.querySelector('input[name="user_type"]').value);

}
