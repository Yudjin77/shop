function showFormErrors(errors, formElement) {
  if (!formElement) {
    console.error('formElement не передан в showFormErrors');
    return;
  }

  // Удаляем старые ошибки только в этой форме
  formElement.querySelectorAll('.form-error').forEach(el => el.remove());

  for (const [fieldName, errorList] of Object.entries(errors)) {
    const messages = errorList.map(err => err.message ?? err); // учитываем как объекты, так и строки

    if (fieldName === '__all__') {
      const generalErrorEl = document.createElement('div');
      generalErrorEl.className = 'form-error';
      generalErrorEl.style.color = 'red';
      generalErrorEl.textContent = messages.join(', ');
      formElement.prepend(generalErrorEl);
      continue;
    }

    const field = formElement.querySelector(`[name="${fieldName}"]`);
    if (field) {
      const errorEl = document.createElement('div');
      errorEl.className = 'form-error';
      errorEl.style.color = 'red';
      errorEl.textContent = messages.join(', ');

      const container = field.closest('.form-group') || field.parentNode;
      container.appendChild(errorEl);
    }
  }
}

// Форма логина
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  try {
    const response = await fetch('/users/login/', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    });

    const data = await response.json();

    if (response.ok) {
      if (data.success) {
        console.log('Login success');
        document.getElementById('loginModal').style.display = 'none';
        location.reload(); // обновляем страницу
      } else {
        console.log('Form errors:', data.errors);
        showFormErrors(data.errors, form);
      }
    } else {
      console.log('Validation errors:', data.errors);
      showFormErrors(data.errors, form);
    }

  } catch (err) {
    console.error('Network or server error:', err);
  }
});


// Форма регистрации
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
        location.reload(); // обновляем страницу
      } else {
        console.log('Form errors:', data.errors);
        showFormErrors(data.errors, form);
      }
    } else {
      console.log('Validation errors:', data.errors);
      showFormErrors(data.errors, form);
    }

  } catch (err) {
    console.error('Network or server error:', err);
  }
});