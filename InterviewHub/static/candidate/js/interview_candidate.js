let currentTaskIndex = 0;
const timerElement = document.getElementById('timer');
const tasks = initialData.tasks;
const isEditable = initialData.isEditable;
let timeLeft = initialData.duration * 60;

// Таймер: обновление и запуск
function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    if (isEditable && timeLeft > 0) {
        timeLeft--;
    } else if (timeLeft === 0) {
        clearInterval(timerInterval);
        alert("Время истекло!");
        submitAllTasks();
    }
}

// Запуск таймера, если редактирование разрешено
if (isEditable) {
    timerElement.style.display = "block"; // Показываем таймер
    const timerInterval = setInterval(updateTimer, 1000);
} else {
    timerElement.style.display = "none"; // Скрываем таймер
    updateTimer(); // Просто отображаем оставшееся время
}


// Изменение кнопки отправки
function configureSubmitButton() {
    const submitButton = document.getElementById('submit-code');
    if (isEditable) {
        submitButton.textContent = "Отправить";
        submitButton.disabled = false;
        submitButton.style.cursor = "pointer";
        submitButton.addEventListener('click', async () => {
            await submitAllTasks();
        });
    } else {
        submitButton.textContent = "Вернуться в меню";
        submitButton.disabled = false;
        submitButton.style.cursor = "pointer";
        submitButton.addEventListener('click', () => {
            window.location.href = "/account/";
        });
    }
}

// Настройка кнопки отправки
configureSubmitButton();

// Обновление текущего задания
function updateTask() {
    const task = tasks[currentTaskIndex];
    document.getElementById('task-title').textContent = task.title;
    document.getElementById('task-description').textContent = task.description;

    // Отображение разных типов заданий
    document.getElementById('editor-pane').style.display = task.type === "code" ? "block" : "none";
    document.getElementById('options-pane').style.display = task.type === "multiple-choice" ? "block" : "none";
    document.getElementById('open-question-pane').style.display = task.type === "open-question" ? "block" : "none";

    if (task.type === "code") {
        const codeEditor = document.getElementById('code-editor');
        codeEditor.value = task.code || "";
        codeEditor.disabled = !isEditable;
        document.getElementById('run-code').style.display = isEditable ? "inline-block" : "none";
    } else {
        document.getElementById('run-code').style.display = "none";
    }

    if (task.type === "multiple-choice") {
        const optionsList = document.getElementById('options-list');
        optionsList.innerHTML = '';
        const selectedAnswers = task.selected_option ? task.selected_option.split(" | ") : [];

        task.options.forEach((option, index) => {
            const isChecked = selectedAnswers.includes(index.toString()) ? "checked" : "";
            const disabled = !isEditable ? "disabled" : "";
            const li = document.createElement('li');
            li.innerHTML = `<label>
                <input type="checkbox" name="option" value="${index}" ${isChecked} ${disabled}>
                ${option.text}
            </label>`;
            optionsList.appendChild(li);
        });
    } else if (task.type === "open-question") {
        const openAnswer = document.getElementById('open-answer');
        openAnswer.value = task.answer || "";
        openAnswer.disabled = !isEditable;
    }

    document.getElementById('prev-task').style.display = currentTaskIndex === 0 ? "none" : "inline-block";
    document.getElementById('next-task').style.display = currentTaskIndex === tasks.length - 1 ? "none" : "inline-block";
}

// Сохранение текущего задания
async function saveTask() {
    if (!isEditable) return;

    const task = tasks[currentTaskIndex];
    const payload = {
        interview_id: task.interview_id,
        task_id: task.id,
        candidate_answer: ""
    };

    if (task.type === "code") {
        payload.candidate_answer = document.getElementById('code-editor').value;
    } else if (task.type === "open-question") {
        payload.candidate_answer = document.getElementById('open-answer').value;
    } else if (task.type === "multiple-choice") {
        const selectedOptions = Array.from(
            document.querySelectorAll('input[name="option"]:checked')
        ).map(option => option.value);
        payload.candidate_answer = selectedOptions.join(" | ");
    }

    task.candidate_answer = payload.candidate_answer;
    console.log(payload.candidate_answer);
    try {
        await fetch("/interview-tasks/save-tasks/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ tasks: [payload] })
        });
    } catch (error) {
        console.error("Ошибка сохранения данных:", error);
    }
}

// Сохранение всех заданий
async function submitAllTasks() {
    if (!isEditable) return;

    await saveTask();
    alert("Все задачи успешно сохранены!");
    window.location.href = "/account/";

}

// Навигация между заданиями
document.getElementById('prev-task').addEventListener('click', async () => {
    if (currentTaskIndex > 0) {
        await saveTask();
        currentTaskIndex--;
        updateTask();
    }
});

document.getElementById('next-task').addEventListener('click', async () => {
    if (currentTaskIndex < tasks.length - 1) {
        await saveTask();
        currentTaskIndex++;
        updateTask();
    }
});

// Запуск кода
document.getElementById('run-code').addEventListener('click', () => {
    alert("Код выполнен! Проверьте консоль.");
});

// Инициализация
updateTask();

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
