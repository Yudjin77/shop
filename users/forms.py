from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        max_length=256,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email',
            'required': False  # Отключаем HTML5 required
        }),
        error_messages={
            'required': 'Пожалуйста, введите email',
            'invalid': 'Введите корректный email',
        },
    )

    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя',
            'required': False
        }),
        error_messages={
            'required': 'Пожалуйста, введите имя'
        },
    )

    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите фамилию',
            'required': False
        }),
        error_messages={
            'required': 'Пожалуйста, введите фамилию'
        },
    )

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'required': False
        }),
        error_messages={
            'required': 'Пожалуйста, введите пароль'
        },
    )

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль',
            'required': False
        }),
        error_messages={
            'required': 'Пожалуйста, повторите пароль'
        },
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

# проверка валидности почты
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email

# переопределение ошибок условий пароля
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")

        # Проверка сложности пароля и перевод сообщений
        if password1:
            try:
                validate_password(password1)
            except ValidationError as e:
                for msg in e.messages:
                    translated = self.translate_password_error(msg)
                    self.add_error('password1', translated)
                    self.add_error('password2', translated)

        return cleaned_data
    

    def translate_password_error(self, msg):
        """
        Преобразует стандартные сообщения Django валидаторов пароля
        в пользовательские или переведённые.
        """
        translations = {
            'This password is too short. It must contain at least 8 characters.':
                'Пароль слишком короткий. Минимум 8 символов',
            'This password is too common.':
                'Пароль слишком простой',
            'This password is entirely numeric.':
                'Пароль не должен состоять только из цифр',
        }
        return translations.get(msg, msg)

# переопределение ошибки не соответсвтия паролей
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают. Убедитесь, что вы ввели одинаковые значения.")
        
        return password2

class CustomUserLoginForm(AuthenticationForm):
    """
    Форма логина через email вместо username
    """

    username = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })

# Profile Form
class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(max_length=50, required=False)
    country = forms.CharField(max_length=50, required=False)
    province = forms.CharField(max_length=50, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    phone = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address1', 'address2',
                  'city', 'country', 'province', 'postal_code', 'phone']
        




