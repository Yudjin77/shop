from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=256, 
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Введите ваш email',
                                 'required': False  # Отключаем HTML5 required
                                 }),
                                 error_messages={
                                     'required': 'Пожалуйста, введите email',
                                     'invalid': 'Введите корректный email',},)
    
    first_name = forms.CharField(required=True, max_length=50,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'Введите имя',
                                     'required': False
                                     }),
                                error_messages={'required': 'Пожалуйста, введите имя'},)
    
    last_name = forms.CharField(required=True, max_length=50, 
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите фамилию',
                                    'required': False
                                    }),
                                error_messages={'required': 'Пожалуйста, введите фамилию'},)

    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Введите пароль',
                                    'required': False}),
                                    error_messages={
                                        'required': 'Пожалуйста, введите пароль'},)
    
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'Повторите пароль',
                                    'required': False}),
                                    error_messages={
                                        'required': 'Пожалуйста, повторите пароль'},)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

# проверка уникальности почты при регестрации
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
            'autofocus': True,
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

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Неверный email или пароль.')  # ТВОЙ ТЕКСТ
            elif not self.user_cache.is_active:
                raise forms.ValidationError('Этот аккаунт отключен.')

        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user_cache', None)




class CusstomUserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваше имя.'})
                                )
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваша фамилия.'})
                                )
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваш email.'})
                                )
    phone = forms.CharField(max_length=150, required=False, 
                            widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'placeholder': 'Ваш телефон.'})
                                )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','address1', 'address2','city', 
                  'country', 'province', 'postal_code', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш телефон.'
            },),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша фамилия',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email.',
            }),
            'address1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш адресс №1'
            }),
            'address2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваша адресс №2'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш город.'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placehodler': 'Ваша страна.'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'placehodler': 'Ваш область.'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placehodler': 'Ваш почтовый индекс.'
            }),
            }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('Этот email уже зарегистрирован')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email

            for field in ['first_name', 'last_name', 'email','address1', 'address2','city', 
                  'country', 'province', 'postal_code', 'phone']:
                if cleaned_data.get(field):
                    cleaned_data[field] = strip_tags(cleaned_data[field])
    

