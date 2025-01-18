document.addEventListener("DOMContentLoaded", function () {
    // Пример динамической обработки для полей формы, если это необходимо
    const startTimeInput = document.querySelector("input[name='start_time']");
    const endTimeInput = document.querySelector("input[name='end_time']");

    // Убедимся, что время окончания не может быть раньше времени начала
    startTimeInput.addEventListener("change", function () {
        const startTime = new Date(startTimeInput.value);
        const endTime = new Date(endTimeInput.value);

        if (endTime <= startTime) {
            alert("Время окончания интервью должно быть позже времени начала.");
            endTimeInput.value = "";  // Очистим поле окончания
        }
    });

    endTimeInput.addEventListener("change", function () {
        const startTime = new Date(startTimeInput.value);
        const endTime = new Date(endTimeInput.value);

        if (endTime <= startTime) {
            alert("Время окончания интервью должно быть позже времени начала.");
            endTimeInput.value = "";  // Очистим поле окончания
        }
    });
});
