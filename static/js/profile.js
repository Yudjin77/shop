document.addEventListener('DOMContentLoaded', () => {
  const editBtn = document.getElementById('edit-profile-btn');
  const form = document.getElementById('edit-profile-form');
  const messages = document.getElementById('form-messages');

  if (!editBtn || !form) {
    console.error('Не найден editBtn или форма');
    return;
  }

  editBtn.addEventListener('click', () => {
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
    messages.innerHTML = '';
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      const response = await fetch('/users/update/', {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      const data = await response.json();
      messages.innerHTML = '';
      document.querySelectorAll('.form-error').forEach(el => el.remove());

      if (response.ok && data.success) {
        messages.innerHTML = '<p style="color: green;">Данные обновлены успешно.</p>';
        form.style.display = 'none';
        location.reload();
      } else if (data.errors) {
        for (const [field, errors] of Object.entries(data.errors)) {
          const input = document.querySelector(`[name="${field}"]`);
          const errorDiv = document.createElement('div');
          errorDiv.className = 'form-error';
          errorDiv.style.color = 'red';
          errorDiv.textContent = errors.join(', ');

          if (input) {
            input.after(errorDiv);
          } else {
            messages.innerHTML += `<p style="color: red;">${errors.join(', ')}</p>`;
          }
        }
      }
    } catch (err) {
      messages.innerHTML = '<p style="color: red;">Произошла ошибка. Попробуйте позже.</p>';
    }
  });
});