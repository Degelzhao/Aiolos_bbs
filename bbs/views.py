from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .models import Question, Choice
from .forms import ChoiceForm, QuestionForm
from accounts.models import UserProfile

# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    query = request.GET.get('q')
    if query:
        query = query.replace('.', '-')
    print(query)
    if query:
        latest_question_list = latest_question_list.filter(
            Q(question_text__icontains=query) |
            Q(author__username__icontains=query) |
            Q(pub_date__icontains=query)
        ).distinct()

    form = QuestionForm()
    context = {
        'latest_question_list': latest_question_list,
        'current_user': {'user': request.user, 'is_login': request.user.is_authenticated},
        'form': form
        }
    return render(request, 'bbs/index.html', context)


class QuestionListView(ListView):
    model = Question
    context_object_name = 'latest_question_list'
    template_name = 'bbs/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = {
            'user': self.request.user, 
            'is_login': self.request.user.is_authenticated}
        context['form'] = QuestionForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            query = query.replace('.', '-')
        # print(query)
        if query:
            latest_question_list = latest_question_list.filter(
                Q(question_text__icontains=query) |
                Q(author__username__icontains=query) |
                Q(pub_date__icontains=query)
            ).distinct()
        return queryset.order_by('-pub_date')


@login_required
def my_page(request):
    latest_question_list = Question.objects.order_by('-pub_date').filter(author=request.user)
    form = QuestionForm()
    context = {
        'latest_question_list': latest_question_list,
        'current_user': {'user': request.user, 'is_login': request.user.is_authenticated},
        'form': form
        }
    return render(request, 'bbs/my_page.html', context)


def detail(request, question_id):
    latest_question_list = Question.objects.order_by('-pub_date')
    all_user_list = UserProfile.objects.order_by('id')
    form = ChoiceForm()
    question = get_object_or_404(Question, pk=question_id)
    choice_list = question.choice_set.all()
    for i in range(0, len(choice_list)):
        for j in range(0, len(all_user_list)):
            if choice_list[i]:
                if choice_list[i].author_id == all_user_list[j].user_id:
                    choice_list[i].user_picture = all_user_list[j].picture
    context = {
        'latest_question_list': latest_question_list,
        'question': question,
        'current_user': {'user': request.user, 'is_login': request.user.is_authenticated},
        'form': form,
        'choice_list': choice_list
        }
    return render(request, 'bbs/detail.html', context)


class DetailListView(ListView):
    model = Question
    context_object_name = 'latest_question_list'
    template_name = 'bbs/detail.html'
    # paginate_by = 5
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_user_list = UserProfile.objects.order_by('id')
        question = get_object_or_404(Question, pk=self.kwargs.get('question_id'))      
        choice_list = question.choice_set.all()
        context_object_name = choice_list
        for i in range(0, len(choice_list)):
            for j in range(0, len(all_user_list)):
                if choice_list[i]:
                    if choice_list[i].author_id == all_user_list[j].user_id:
                        choice_list[i].user_picture = all_user_list[j].picture
        context['current_user'] = {
            'user': self.request.user, 
            'is_login': self.request.user.is_authenticated}
        context['form'] = ChoiceForm()
        context['choice_list'] = choice_list
        context['question'] = question
        p = Paginator(choice_list, 5)
        context['paginator'] = p
        context['is_paginated'] = True
        if self.request.GET.get('page'):
            i = self.request.GET.get('page')
        else:
            i = 1
        context['page_obj'] = p.page(i)

        print(context, p.num_pages)
        return context

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset

# class DetailListView(DetailView):
#     model = Question
#     context_object_name = 'latest_question_list'
#     template_name = 'bbs/detail.html'
#     paginate_by = 10
 
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         all_user_list = UserProfile.objects.order_by('id')
#         pk = self.kwargs.get(self.pk_url_kwarg, None)
#         question = get_object_or_404(Question, pk=pk)      
#         choice_list = question.choice_set.all()
#         for i in range(0, len(choice_list)):
#             for j in range(0, len(all_user_list)):
#                 if choice_list[i]:
#                     if choice_list[i].author_id == all_user_list[j].user_id:
#                         choice_list[i].user_picture = all_user_list[j].picture
#         context['current_user'] = {
#             'user': self.request.user, 
#             'is_login': self.request.user.is_authenticated}
#         context['form'] = ChoiceForm()
#         context['choice_list'] = choice_list
#         return context

@login_required
def topic(request):
    # 取到数据
    latest_question_list = Question.objects.order_by('-pub_date')
    if request.method == 'POST':
        # 判断pk存在的情况下，只更新数据
        pk = request.POST.get('pk')
        if pk:
            question = get_object_or_404(Question, pk=pk)
            print('get question by pk: ', pk, question)
            question.question_text = request.POST['question_text']
            question.question_desc = request.POST['question_desc']
            question.save()
            return HttpResponseRedirect(reverse('bbs:detail', args=(pk,)))

        form = QuestionForm(request.POST, request.FILES or None)
        print('form:', form, request.FILES)
        # 判断合法，并保存
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            if request.FILES:
                picture_name = str(request.FILES['picture'])
                if picture_name.endswith('.jpg') or picture_name.endswith('.png'):
                    question.save()
                else:
                    return render(request, 'bbs/index.html', {
                    'latest_question_list': latest_question_list,
                    'form': form,
                    'current_user': {'user': request.user, 'is_login': request.user.is_authenticated},
                    'error_message': "图片格式不正确"})
            else:
                question.save()           
    # 返回页面
    return HttpResponseRedirect(reverse('bbs:index'))


@method_decorator(login_required, name='dispatch')
class TopicUpdateView(UpdateView):
    model = Question
    template_name = 'bbs/detail.html'

    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        if pk:
            question = get_object_or_404(Question, pk=pk)
            print('get question by pk: ', pk, question)
            question.question_text = request.POST['question_text']
            question.question_desc = request.POST['question_desc']
            question.save()
            return HttpResponseRedirect(reverse('bbs:detail', args=(pk,)))


class TopicCreateView(CreateView):
    model = Question
    template_name = 'bbs/index.html'
    fields = ('question_text', 'question_desc', 'picture')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_question_list'] = self.model.objects.order_by('-pub_date')
        context['current_user'] = {
            'user': self.request.user, 
            'is_login': self.request.user.is_authenticated}
        context['form'] = QuestionForm()
        if self.request.FILES:
            picture_name = str(self.request.FILES['picture'])
            if picture_name.endswith('.bmp') or picture_name.endswith('.gif'):
                context['error_message'] = '图片格式不正确'
        return context

    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        if self.request.POST['question_desc']:
            question.question_desc = self.request.POST['question_desc']
        if self.request.FILES:
            picture_name = str(self.request.FILES['picture'])
            if picture_name.endswith('.jpg') or picture_name.endswith('.png'):
                question.save()
            else:
                c = self.get_context_data()
                return render(self.request, 'bbs/index.html', c)
        else:
            question.save()
        return redirect('bbs:index')


# def reply_old(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         reply_name = request.POST['reply_name']
#         reply_text = request.POST['reply_text']
#         print(reply_name, reply_text)

#         if reply_name and reply_text:
#             question.choice_set.create(
#                 choice_text = reply_text,
#                 author = reply_name
#             )
#             question.save()
#         else:
#             return render(request, 'bbs/detail.html', {
#             'question': question,
#             'error_message': "没有数据！",
#         })
#     except (KeyError):
#         # Redisplay the question voting form.
#         return render(request, 'bbs/detail.html', {
#             'question': question,
#             'error_message': "传值出错！！",
#         })
#     else:
#         return HttpResponseRedirect(reverse('bbs:detail', args=(question.id,)))


def reply(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        if request.method == 'POST':
            form = ChoiceForm(request.POST, request.FILES or None)
            print('form:', form, request.FILES)
            if form.is_valid():
                reply = form.save(commit=False)
                print('reply: ', reply, type(reply))
                reply.author = request.user
                reply.question = question
                # reply.picture = request.FILES['picture']
                if request.FILES:
                    picture_name = str(request.FILES['picture'])
                    if picture_name.endswith('.jpg') or picture_name.endswith('.png'):
                        reply.save()
                    else:
                        return render(request, 'bbs/detail.html', {
                        'question': question,
                        'form': form,
                        'current_user': {'user': request.user, 'is_login': request.user.is_authenticated},
                        'error_message': "图片格式不正确"})
                else:
                    reply.save()

    except (KeyError):
        # Redisplay the question voting form.
        return render(request, 'bbs/detail.html', {
            'question': question,
            'error_message': "传值出错！！",
        })
    else:
        return HttpResponseRedirect(reverse('bbs:detail', args=(question.id,)))

    