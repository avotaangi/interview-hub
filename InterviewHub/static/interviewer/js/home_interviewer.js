// Update the status and comment in the form based on the card's initial status and comment
document.querySelectorAll('.card').forEach(card => {
    const statusSelect = card.querySelector('.status-select');
    const commentsField = card.querySelector('.comments');
    const statusText = card.querySelector('.status');
    const commentText = card.querySelector('.comment-text');
    const updateForm = card.querySelector('.update-status-form');
    const interviewId = card.getAttribute('data-id'); // Предположим, что ID интервью хранится в data-id

    updateForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        const newStatus = statusSelect.value;
        const newComment = commentsField.value;

        const currentStatus = newStatus.split("|")[1];
        const currentStatusClass = newStatus.split("|")[0];

        try {
            const response = await fetch(`/interviews/${interviewId}/update-status/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // Получение CSRF-токена
                },
                body: JSON.stringify({
                    status: currentStatus,
                    feedback: newComment,
                }),
            });

            if (response.ok) {
                const data = await response.json();

                // Обновление интерфейса
                statusText.classList.remove('approved', 'rejected', 'pending');
                statusText.classList.add(currentStatusClass);
                statusText.textContent =
                    currentStatusClass === 'approved' ? 'Одобрено' :
                    currentStatusClass === 'rejected' ? 'Не одобрено' :
                    'На рассмотрении';

                commentText.textContent = data.feedback || 'Комментарий отсутствует.';
            } else {
                alert('Ошибка при обновлении статуса. Проверьте данные.');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке запроса.');
        }
    });
});

// Функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверяем, совпадает ли имя cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Открыть модальное окно при клике на кнопку
const openModalButton = document.getElementById('openModalButton');
const scheduleModal = document.getElementById('scheduleModal');
const closeModalButton = document.getElementById('closeModalButton');

openModalButton.addEventListener('click', () => {
    scheduleModal.style.display = 'flex';  // Показываем модальное окно
});

// Закрыть модальное окно
closeModalButton.addEventListener('click', () => {
    scheduleModal.style.display = 'none';  // Скрываем модальное окно
});

// Закрыть модальное окно, если кликнут в область за пределами модального окна
window.addEventListener('click', (event) => {
    if (event.target === scheduleModal) {
        scheduleModal.style.display = 'none';
    }
});

scheduleForm.addEventListener('submit', async function (e) {
    e.preventDefault(); // Отменяем стандартное поведение формы

    // Собираем данные из формы
    const resumeId = parseInt(document.getElementById('candidateName').value); // Теперь это resume_id
    const userId = AUTH_USER_ID; // Переменная AUTH_USER_ID должна быть определена сервером как ID авторизованного пользователя
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const duration = document.getElementById('duration').value;
    const type = document.getElementById('type').value;
    const tasks = Array.from(document.querySelectorAll('.task-select')).map(task => task.value);
    const link = document.getElementById('link').value;

    const getUserData = async (userId) => {
        try {
            const response = await fetch(`/user/${userId}/user-data/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Ошибка получения данных пользователя');
            }

            const data = await response.json();
            return data.interview ? data.interview.id : null; // Возвращаем interviewId или null
        } catch (error) {
            console.error('Ошибка получения данных пользователя:', error);
            throw error;
        }
    };

    const interviewerId = await getUserData(userId);

    // Формируем тело запроса для создания CompanySelection
    const selectionPayload = {
        interviewer_id: interviewerId,
        resume_id: resumeId,
        status: "На рассмотрении" // Устанавливаем статус по умолчанию
    };

    console.log(selectionPayload);

    const csrfToken = getCookie('csrftoken'); // Убедитесь, что функция getCookie() извлекает CSRF-токен
    try {
        // Создаем запись CompanySelection
        const selectionResponse = await fetch('/company-selections/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(selectionPayload)
        });

        if (!selectionResponse.ok) {
            throw new Error('Ошибка создания CompanySelection');
        }

        const selectionData = await selectionResponse.json();

        // Формируем тело запроса для создания Interview
        const startTime = `${date}T${time}`;
        const endTime = new Date(new Date(startTime).getTime() + duration * 60000).toISOString(); // Расчет времени окончания
        console.log(selectionData.id)
        const interviewPayload = {
            selection: selectionData.id,
            start_time: startTime,
            end_time: endTime,
            duration: parseInt(duration),
            type: type,
            status: "Запланировано",
            additional_url: link
        };

        console.log(interviewPayload);

        // Создаем запись Interview
        const interviewResponse = await fetch('/interviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(interviewPayload)
        });

        if (!interviewResponse.ok) {
            throw new Error('Ошибка создания Interview');
        }

        const interviewData = await interviewResponse.json();

        // Создаем записи InterviewTaskItem
        for (const taskId of tasks) {
            const taskPayload = {
                interview: interviewData.id,
                task_item: parseInt(taskId),
                candidate_answer: "" // Оставляем пустым для заполнения позже
            };
            console.log(taskPayload)

            const taskResponse = await fetch('/interview-tasks/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(taskPayload)
            });

            if (!taskResponse.ok) {
                throw new Error('Ошибка создания InterviewTaskItem');
            }
        }

        // Формируем HTML для нового блока
        const interviewCard = document.createElement('div');
        interviewCard.classList.add('card_one');

        const tasksList = tasks.map(taskId => `<span>${taskId}</span>`).join(', '); // Модифицируйте отображение задач по необходимости

        interviewCard.innerHTML = `
            <p><strong>Дата:</strong> ${new Date(interviewData.start_time).toISOString().split('T')[0]}</p>
            <p><strong>Время:</strong> ${new Date(interviewData.start_time).toISOString().split('T')[1].slice(0, 5)}</p>
            <p><strong>Кандидат:</strong> ${resumeId}</p>
            <p><strong>Тип интервью:</strong> ${interviewData.type}</p>
            <p><strong>Назначенные задания:</strong> ${tasksList}</p>
            <p><strong>Ссылка на подключение:</strong>
                <a href="${interviewData.additional_url}" target="_blank">${interviewData.additional_url}</a>
            </p>
            <a href="${selectionData.resume.file}" download>
                <button>Посмотреть резюме</button>
            </a>
            <button class="cancel-interview-button red-button">Отменить собеседование</button>
        `;

        const upcomingInterviewsContainer = document.querySelector('.section');

        // Добавляем новый блок в раздел «Предстоящие собеседования»
        upcomingInterviewsContainer.appendChild(interviewCard);

        // Уведомление об успешном создании
        alert('Интервью успешно запланировано.');

        // Скрываем модальное окно
        scheduleModal.style.display = 'none';

        // Очищаем форму для следующего использования
        scheduleForm.reset();
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при планировании интервью. Попробуйте снова.');
    }
});



const tasksContainer = document.getElementById("tasks-container");
const addTaskButton = document.getElementById("add-task-button");

// Функция для загрузки данных о задачах
async function fetchTasks() {
    try {
        const response = await fetch("/task-items/"); // Замените на ваш актуальный URL
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        const tasks = await response.json();
        console.log(tasks);
        return tasks;
    } catch (error) {
        console.error("Ошибка при загрузке задач:", error);
        return [];
    }
}

// Функция для создания строки задания
function createTaskRow(tasks) {
    const taskRow = document.createElement("div");
    taskRow.className = "task-row";

    // Создаем выпадающий список
    const selectElement = document.createElement("select");
    selectElement.name = "tasks[]";
    selectElement.className = "task-select";
    selectElement.required = true;

    // Добавляем опции в выпадающий список
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = "Выберите задание";
    selectElement.appendChild(defaultOption);

    tasks.forEach(task => {
        const option = document.createElement("option");
        option.value = task.id;
        option.textContent = task.title.length > 30
            ? task.title.substring(0, 27) + "..."
            : task.title;
        selectElement.appendChild(option);
    });

    // Создаем кнопку удаления
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "remove-task-button";
    removeButton.textContent = "✖";
    removeButton.addEventListener("click", function () {
        tasksContainer.removeChild(taskRow);
    });

    // Добавляем элементы в строку задания
    taskRow.appendChild(selectElement);
    taskRow.appendChild(removeButton);

    return taskRow;
}

// Добавление нового задания при клике на кнопку
addTaskButton.addEventListener("click", async function () {
    const tasks = await fetchTasks(); // Загружаем задачи через API
    if (tasks.count > 0) {
        const taskRow = createTaskRow(tasks.results);
        tasksContainer.appendChild(taskRow);
    } else {
        alert("Нет доступных задач для выбора.");
    }
});

function removeTask(button) {
    const taskRow = button.parentElement;
    tasksContainer.removeChild(taskRow);
}

// Функция для обработки клика на кнопку "Отменить собеседование"
document.querySelectorAll('.cancel-interview-button').forEach(button => {
    button.addEventListener('click', async function () {
        const card = button.closest('.card_one');
        const interviewId = card.getAttribute('data-id');
        const csrfToken = getCookie('csrftoken'); // Убедитесь, что функция getCookie() определена

        if (confirm('Вы уверены, что хотите отменить это собеседование?')) {
            try {
                const response = await fetch(`/interviews/${interviewId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                });

                if (response.ok) {
                    // Удаляем карточку из DOM
                    card.remove();
                    alert('Собеседование успешно отменено.');
                } else {
                    alert('Ошибка при отмене собеседования. Попробуйте снова.');
                }
            } catch (error) {
                console.error('Ошибка при отмене собеседования:', error);
                alert('Произошла ошибка. Попробуйте позже.');
            }
        }
    });
});

