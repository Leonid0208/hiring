from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import View
from .models import Chat, Candidate
from .forms import MessageForm, CreateResumeForm
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


def main(request):
    resumes = Candidate.objects.all()

    return render(request, 'desk/main.html', {'posts': resumes})


class DialogsView(LoginRequiredMixin, View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'desk/dialogs.html', {'user_profile': request.user, 'chats': chats})


class MessagesView(LoginRequiredMixin, View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'desk/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class CreateDialogView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('messages', kwargs={'chat_id': chat.id}))


class CreateResume(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.account_type == 'candidate':
            create_form = CreateResumeForm()
            return render(request, 'desk/create_resume.html', {'form': create_form})
        else:
            return HttpResponse('Go away')

    def post(self, request):
        create_form = CreateResumeForm(request.POST)
        if create_form.is_valid():
            resume = create_form.save(commit=False)
            resume.user = request.user
            resume.save()
            print('Mb save')
        else:
            print('Not save')
        return redirect(reverse('desk'))





