from django.shortcuts import render

def index(request):
    return render(
        request,
        'samvera/index.html',
        {
            'title': 'Нашёл чего интересного?',
            'message': 'Здаров чувак, смотрю пытаешься доступ получить? Как успехи? Может расскажешь что и как делаешь? \
            Какой софт используешь, хотя это скорее скрипты у тебя... \
            Нафиг тебе мой phpMyAdmin? Нужны данные? Попахивает воровством, не так ли?'
        }
    )