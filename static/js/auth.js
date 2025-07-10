function showFormErrors(errors) {
  // Удаляем все старые ошибки
  document.querySelectorAll('.form-error').forEach(el => el.remove());

  for (const [fieldName, errorList] of Object.entries(errors)) {
    const messages = errorList.map(err => err.message); // <-- вытаскиваем message из объекта

    if (fieldName === '__all__') {
      // Общие ошибки формы, можно показать сверху или снизу
      const generalErrorEl = document.createElement('div');
      generalErrorEl.className = 'form-error';
      generalErrorEl.style.color = 'red';
      generalErrorEl.textContent = messages.join(', ');
      document.getElementById('registerForm').prepend(generalErrorEl);
      continue;
    }

    const field = document.querySelector(`[name="${fieldName}"]`);
    if (field) {
      const errorEl = document.createElement('div');
      errorEl.className = 'form-error';
      errorEl.style.color = 'red';
      errorEl.textContent = messages.join(', ');

      if (field.parentNode.classList.contains('form-group')) {
        field.parentNode.appendChild(errorEl);
      } else {
        field.after(errorEl);
      }
    }
  }
}

// Форма логина
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const response = await fetch('/users/login/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  });

  if (response.ok) {
    const data = await response.json();
    if (data.success) {
      console.log('Login success');
      document.getElementById('loginModal').style.display = 'none';
      location.reload();
    } else {
      console.log('Form errors:', data.errors);
      showFormErrors(data.errors);
    }
  } else {
    console.error('HTTP error:', response.status);
  }
});

// Форма регистрации
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  const response = await fetch('/users/register/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-Requested-With': 'XMLHttpRequest'
    }
  });

  if (response.ok) {
    const data = await response.json();
    if (data.success) {
      console.log('Register success');
      document.getElementById('registerModal').style.display = 'none';
      location.reload();
    } else {
      console.log('Form errors:', data.errors);
      showFormErrors(data.errors);
    }
  } else {
    console.error('HTTP error:', response.status);
  }
});

document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  try {
    const response = await fetch('/users/register/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });

    const data = await response.json();

    if (response.ok) {
      if (data.success) {
        console.log('Register success');
        document.getElementById('registerModal').style.display = 'none';
        location.reload();
      } else {
        console.log('Form errors:', data.errors);
        showFormErrors(data.errors);
      }
    } else {
      // тут обрабатываем ошибки валидации, даже если код 400
      console.log('Validation errors:', data.errors);
      showFormErrors(data.errors);
    }

  } catch (err) {
    console.error('Network or server error:', err);
  }
});