// main.js — работа с модалками и панелью категорий
document.addEventListener('DOMContentLoaded', () => {
  const loginButton    = document.getElementById('loginButton');
  const loginModal     = document.getElementById('loginModal');
  const registerModal  = document.getElementById('registerModal');
  const navBtn         = document.getElementById('categories-button');
  const navPanel       = document.getElementById('categories-panel');

  // Открыть окно логина
  loginButton.addEventListener('click', () => {
    loginModal.style.display = 'flex';
  });

  // Показать окно регистрации из логина
  document.getElementById('showRegister').addEventListener('click', () => {
    loginModal.style.display    = 'none';
    registerModal.style.display = 'flex';
  });

  // Показать окно логина из регистрации
  document.getElementById('showLogin').addEventListener('click', () => {
    registerModal.style.display = 'none';
    loginModal.style.display    = 'flex';
  });

  // Закрытие модалки по клику вне контента
  [loginModal, registerModal].forEach(modal => {
    modal.addEventListener('click', e => {
      if (e.target === modal) modal.style.display = 'none';
    });
  });

  // Панель категорий
  navBtn.addEventListener('click', () => {
    navPanel.style.display = navPanel.style.display === 'block' ? 'none' : 'block';
  });
  document.addEventListener('click', (e) => {
    if (!navBtn.contains(e.target) && !navPanel.contains(e.target)) {
      navPanel.style.display = 'none';
    }
  });
});