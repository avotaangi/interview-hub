let currentTaskIndex = 0;
const timerElement = document.getElementById('timer');
const tasks = initialData.tasks;
let timeLeft = initialData.duration * 60;

// Обновление таймера
function updateTimer() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    if (timeLeft > 0) {
        timeLeft--;
    } else {
        clearInterval(timerInterval);
        alert("Время истекло!");
        submitAllTasks(); // Автоматическое сохранение всех задач
    }
}

const timerInterval = setInterval(updateTimer, 1000);

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
        document.getElementById('code-editor').value = task.code || "";
        document.getElementById('run-code').style.display = "inline-block";
    } else {
        document.getElementById('run-code').style.display = "none";
    }

    if (task.type === "multiple-choice") {
        const optionsList = document.getElementById('options-list');
        optionsList.innerHTML = '';

        // Разделяем сохраненные ответы
        const selectedAnswers = task.selected_option ? task.selected_option.split(" | ") : [];
        console.log(task.selected_option)
        task.options.forEach((option, index) => {
            const isChecked = selectedAnswers.includes(index.toString()) ? "checked" : "";
            const li = document.createElement('li');
            li.innerHTML = `<label>
                <input type="checkbox" name="option" value="${index}" ${isChecked}>
                ${option.text}
            </label>`;
            optionsList.appendChild(li);
        });
    } else if (task.type === "open-question") {
        document.getElementById('open-answer').value = task.answer || "";
    }

    // Управление видимостью кнопок
    document.getElementById('prev-task').style.display = currentTaskIndex === 0 ? "none" : "inline-block";
    document.getElementById('next-task').style.display = currentTaskIndex === tasks.length - 1 ? "none" : "inline-block";
}

// Сохранение текущего задания
async function saveTask() {
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
        // Собираем выбранные варианты ответа
        const selectedOptions = Array.from(
            document.querySelectorAll('input[name="option"]:checked')
        ).map(option => option.value);
        payload.candidate_answer = selectedOptions.join(" | ");
    }

    task.candidate_answer = payload.candidate_answer;
    console.log(payload);
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
    const payload = tasks.map(task => ({
        interview_id: task.interview_id,
        task_id: task.id,
        candidate_answer: task.candidate_answer || ""
    }));

    try {
        const response = await fetch("/interview-tasks/save-tasks/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken')
            },
            body: JSON.stringify({ tasks: payload })
        });

        if (response.ok) {
            alert("Все задачи успешно сохранены!");
            window.location.href = "/account/"
        } else {
            alert("Ошибка при сохранении задач.");
        }
    } catch (error) {
        console.error("Ошибка сохранения всех данных:", error);
    }
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

// Отправка всех данных
document.getElementById('submit-code').addEventListener('click', async () => {
    await submitAllTasks();
});

// Инициализация первого задания
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
