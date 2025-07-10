//Схема Обработки запросов форм(регистрация, авторизация, изминение профиля)

✅ ИТОГОВАЯ СХЕМА
1️⃣ HTML-форма (в шаблоне)
2️⃣ JS → отправка POST на /register/
3️⃣ Django views.register → принимает POST
4️⃣ Forms.py → валидация
5️⃣ Forms.py → save()
6️⃣ Models.py → CustomUserManager.create_user()
7️⃣ set_password → хеш пароля
8️⃣ save() → запись в БД
9️⃣ JsonResponse → успех или ошибки