from django.http import HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import View
from .models import Chat, Candidate, Message
from .forms import MessageForm, CreateResumeForm
from django.db.models import Count
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from app.models import CustomUser
from hiring.settings import DEFAULT_FROM_EMAIL


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
            chat = Chat.objects.filter(id=chat_id)[0]
            if Message.objects.filter(chat=chat_id).count() == 0:
                users = chat.members.all()
                if users[0] == request.user:
                    user = users[1]
                else:
                    user = users[0]
                # user = CustomUser.objects.filter(id=user_id)[0]
                username = user.username
                email = user.email
                send_mail(
                    'ITBerth Notification',
                    '{name}, you have message from {name_from} {url}'.format(name=username, name_from=request.user.username, url=request.META['HTTP_HOST'] + chat.get_absolute_url()),
                    DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False
                ) 
            message.save()

        return redirect(reverse('messages', kwargs={'chat_id': chat_id}))


class PostView(View):
    def get(self, request, post_id):
        post = Candidate.objects.get(id=post_id)
        return render(
            request,
            'desk/resume_page.html',
            {
                'post': post,
            }
        )



class CreateDialogView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
            chat.save()

            # user = CustomUser.objects.filter(id=user_id)[0]
            # username = user.username
            # email = user.email
            # send_mail(
            #     'ITBerth Notification',
            #     '{name}, you have message from {name_from} {url}'.format(name=username, name_from=request.user.username, url=request.META['HTTP_HOST'] + chat.get_absolute_url()),
            #     DEFAULT_FROM_EMAIL,
            #     [email],
            #     fail_silently=False
            # )
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
        create_form = CreateResumeForm(request.POST, request.FILES or None)
        if create_form.is_valid():
            resume = create_form.save(commit=False)
            resume.user = request.user
            resume.save()
            print('Mb save')
        else:
            print('Not save')
        return redirect(reverse('desk'))





