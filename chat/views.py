from django.shortcuts import render


def chat_page(request):
    return render(request, 'chat/chat.html')

from .models import ChatMessage

def chat_view(request):
    messages = ChatMessage.objects.all().order_by('timestamp')
    return render(request, 'chat.html', {'messages': messages})


# views.py
def chat_view(request):
    # Загружаем старые сообщения из сессии
    chat_messages = request.session.get('chat_messages', [])

    if request.method == 'POST':
        new_message = request.POST.get('message')
        chat_messages.append(new_message)
        request.session['chat_messages'] = chat_messages

    return render(request, 'chat.html', {'messages': chat_messages})

def chat_bot_page(request):
    return render(request, 'chat/chatbot.html')
