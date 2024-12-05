document.addEventListener("DOMContentLoaded", function () {
    let selectedItem = null; // Текущий выбранный компонент

    // Событие: выделение компонента
    document.getElementById("componentList").addEventListener("click", function (e) {
        if (e.target && e.target.matches(".list-group-item")) {
            // Убираем выделение со всех элементов
            document.querySelectorAll(".list-group-item").forEach(item => item.classList.remove("active"));
            // Добавляем выделение на выбранный элемент
            e.target.classList.add("active");
            selectedItem = e.target.getAttribute("data-value"); // Сохраняем выбранное значение
        }
    });

    // Событие: выбор компонента и установка значения в поле
    document.getElementById("selectComponentBtn").addEventListener("click", function () {
        if (selectedItem) {
            // Найти связанное поле для ввода (например, GPU, CPU и т.д.)
            const activeInput = document.querySelector(".form-configurator input:focus");
            if (activeInput) {
                activeInput.value = selectedItem; // Устанавливаем выбранное значение
            }
            // Закрыть модальное окно
            const modal = bootstrap.Modal.getInstance(document.getElementById("modalSelectComponent"));
            modal.hide();
        } else {
            alert("Пожалуйста, выберите компонент из списка.");
        }
    });

    // Фильтрация списка компонентов
    document.getElementById("componentSearch").addEventListener("input", function (e) {
        const filter = e.target.value.toLowerCase();
        document.querySelectorAll("#componentList .list-group-item").forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? "" : "none";
        });
    });
});
