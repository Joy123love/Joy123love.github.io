document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.querySelector('.input-wrapper input');
    const addTaskBtn = document.querySelector('.input-wrapper i'); // Using the plus icon as button
    const tasksList = document.querySelector('.tasks-list');
    const progressCircle = document.querySelector('.circle');
    const progressText = document.querySelector('.percentage');

    // Load tasks from LocalStorage
    let tasks = JSON.parse(localStorage.getItem('tasks')) || [
        { text: "Review project proposal", tag: "Work", completed: true },
        { text: "Buy groceries for dinner", tag: "Personal", completed: false },
        { text: "Call mom", tag: "Family", completed: false },
        { text: "Schedule dentist appointment", tag: "Health", completed: true },
        { text: "Finish reading Chapter 4", tag: "Learning", completed: false }
    ];

    function renderTasks() {
        tasksList.innerHTML = '';
        let completedCount = 0;

        tasks.forEach((task, index) => {
            if (task.completed) completedCount++;

            const label = document.createElement('label');
            label.className = 'task-item';
            
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.checked = task.completed;
            checkbox.addEventListener('change', () => toggleTask(index));

            const checkmark = document.createElement('span');
            checkmark.className = 'checkmark';
            checkmark.innerHTML = '<i class="fa-solid fa-check"></i>';

            const contentDiv = document.createElement('div');
            contentDiv.className = 'task-content';

            const textSpan = document.createElement('span');
            textSpan.className = 'task-text';
            textSpan.textContent = task.text;

            const tagSpan = document.createElement('span');
            tagSpan.className = `task-tag tag-${task.tag.toLowerCase()}`;
            tagSpan.textContent = task.tag;

            // Delete button (new feature)
            const deleteBtn = document.createElement('i');
            deleteBtn.className = 'fa-solid fa-trash delete-btn';
            deleteBtn.style.marginLeft = '10px';
            deleteBtn.style.color = '#ef4444';
            deleteBtn.style.cursor = 'pointer';
            deleteBtn.style.opacity = '0';
            deleteBtn.style.transition = 'opacity 0.2s';
            
            label.addEventListener('mouseenter', () => deleteBtn.style.opacity = '1');
            label.addEventListener('mouseleave', () => deleteBtn.style.opacity = '0');
            deleteBtn.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent label click
                deleteTask(index);
            });

            contentDiv.appendChild(textSpan);
            contentDiv.appendChild(tagSpan);
            contentDiv.appendChild(deleteBtn);

            label.appendChild(checkbox);
            label.appendChild(checkmark);
            label.appendChild(contentDiv);

            tasksList.appendChild(label);
        });

        updateProgress(completedCount, tasks.length);
        saveTasks();
    }

    function addTask(text) {
        if (text.trim() === '') return;
        tasks.unshift({ text: text, tag: "Personal", completed: false }); // Default tag
        renderTasks();
        taskInput.value = '';
    }

    function toggleTask(index) {
        tasks[index].completed = !tasks[index].completed;
        renderTasks();
    }

    function deleteTask(index) {
        tasks.splice(index, 1);
        renderTasks();
    }

    function updateProgress(completed, total) {
        const percentage = total === 0 ? 0 : Math.round((completed / total) * 100);
        progressText.textContent = `${percentage}%`;
        
        // Update circle stroke-dasharray (circumference is approx 100 for pathLength 100 or viewbox calc)
        // The path defined in HTML is a bit complex, let's just update the text for now or try to animate the stroke.
        // The CSS animation 'progress' sets it to 100. We need to set it dynamically.
        // stroke-dasharray="current, 100"
        progressCircle.style.strokeDasharray = `${percentage}, 100`;
    }

    function saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    // Event Listeners
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask(taskInput.value);
        }
    });

    addTaskBtn.style.cursor = 'pointer';
    addTaskBtn.addEventListener('click', () => {
        addTask(taskInput.value);
    });

    // Initial Render
    renderTasks();
});
