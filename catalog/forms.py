from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import *


class SignUpForm(UserCreationForm):
    fio = forms.CharField(widget=forms.TextInput, label='ФИО', help_text='Только буквы кириллицы, дефис и пробелы',
                          validators=[RegexValidator('^[а-яА-ЯёЁ-]+\s+[а-яА-ЯёЁ-]+\s+[а-яА-ЯёЁ-]', message="Неправильное ФИО, пожалуйста, попробуйте снова.")],
                          required=True)
    username = forms.CharField(label='Логин', widget=forms.TextInput, help_text='Только латиница и дефис, уникальный', required=True,
                               validators=[RegexValidator('^[a-zA-Z-]', message = "Неправильный логин, пожалуйста, попробуйте снова.")],
                               error_messages={
                                   'unique': 'Этот логин уже занят, попробуйте пожалуйста другой'
                               })
    email = forms.EmailField(label='Email', widget=forms.EmailInput, help_text='Валидный формат email-адреса', required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=True)
    agree = forms.BooleanField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput, required=True)

    class Meta:
        model = UserProfile
        fields = ('fio', 'username', 'email', 'password1', 'password2', 'agree')


    def clean_password2(self):
        value = self.cleaned_data
        if value['password1'] != value['password2']:
            raise forms.ValidationError("Ошибка! Пароли не совпадают!")
        return value['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Ошибка! Такой E-mail уже существует!")
        return email

class RequestCreateForm(forms.ModelForm):
    name = forms.CharField(label='Заголовок', widget=forms.TextInput, required=True)
    description = forms.CharField(label='Описание', widget=forms.Textarea, required=True)
    category = forms.ModelChoiceField(label='Категория', queryset=Category.objects.all(), required=True)
    image = forms.ImageField(
        label='План вашего помещения', widget=forms.FileInput,
        help_text='Изображения должно быть в одном из форматов (jpg, jpeg, png, bmp) и с максимальным размером 2 МБ',
        required=True)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        image_types = ['.jpg', '.jpeg', '.png', '.bpm']
        for image_type in image_types:
            if image_type in str(image) and image.size <= 2097152:
                return image

        raise forms.ValidationError(
            "Ошибка: "
            "Файл должен иметь формат: jpg, jpeg, png, bmp и размер не более 2МБ"
        )

    class Meta:
        model = Request
        fields = ('name', 'description', 'category', 'image', )

        class RequestWorkStatusChangeForm(forms.ModelForm):
            comment = forms.CharField(label='Комментарий', widget=forms.TextInput, required=True)

            class Meta:
                model = Request
                fields = ('comment',)




