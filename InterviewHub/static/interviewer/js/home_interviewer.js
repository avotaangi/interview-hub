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

// Обработать отправку формы и добавить информацию в «Предстоящие собеседования»
const scheduleForm = document.getElementById('scheduleForm');
const upcomingInterviewsContainer = document.querySelector('.section');

scheduleForm.addEventListener('submit', function (e) {
    e.preventDefault();  // Отменяем стандартное поведение формы

    // Собираем данные из формы
    const candidateName = document.getElementById('candidateName').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const tasks = document.getElementById('tasks').value;
    const link = document.getElementById('link').value;

    // Создаем новый блок для собеседования
    const interviewCard = document.createElement('div');
    interviewCard.classList.add('card_one');

    interviewCard.innerHTML = `
        <p><strong>Дата:</strong> ${date}</p>
        <p><strong>Время:</strong> ${time}</p>
        <p><strong>Кандидат:</strong> ${candidateName}</p>
        <p><strong>Назначенные задания:</strong> ${tasks}</p>
        <p><strong>Ссылка на подключение:</strong> <a href="${link}" target="_blank">${link}</a></p>
        <a href="#" download><button>Скачать резюме</button></a>
    `;

    // Добавляем новый блок в раздел «Предстоящие собеседования»
    upcomingInterviewsContainer.appendChild(interviewCard);

    // Скрываем модальное окно
    scheduleModal.style.display = 'none';

    // Очищаем форму для следующего использования
    scheduleForm.reset();
});