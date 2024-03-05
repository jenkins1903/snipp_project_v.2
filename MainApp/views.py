from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .models import Snippet
from .forms import SnippetForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import SignUpForm
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import LoginView

@csrf_protect
def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@csrf_protect
@login_required
def add_snippet_page(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)  
            snippet.author = request.user      
            snippet.save()                     
            return redirect('view_snippets')   
    else:
        form = SnippetForm()
    context = {'pagename': 'Добавление нового сниппета', 'form': form}
    return render(request, 'pages/add_snippet.html', context)

@csrf_protect
def snippets_page(request):
    if request.method == 'GET':
        snippet_id = request.GET.get('snippet_id')
        if snippet_id:
            return redirect('snippet_detail', id=snippet_id)
    

    language = request.GET.get('lang', '')
    sort = request.GET.get('sort', 'creation_date')  

    if sort not in ['name', 'creation_date', 'language']:  
        sort = 'creation_date'  
    if request.user.is_authenticated:
        if language:  
            snippets = Snippet.objects.filter(
                (Q(is_public=True) | Q(author=request.user)) & Q(lang=language)
            ).order_by(sort)
        else:  
            snippets = Snippet.objects.filter(Q(is_public=True) | Q(author=request.user)).order_by(sort)
    else:
        if language:  
            snippets = Snippet.objects.filter(is_public=True, lang=language).order_by(sort)
        else:  
            snippets = Snippet.objects.filter(is_public=True).order_by(sort)

    languages = Snippet.objects.values_list('lang', flat=True).distinct()
    return render(request, 'pages/view_snippets.html', {'snippets': snippets, 'languages': languages, 'selected_language': language, 'current_sort': sort})


@csrf_protect
def snippet_detail(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    comment_form = CommentForm()  
    context = {
        'snippet': snippet,
        'comment_form': comment_form  
    }
    return render(request, 'pages/snippet_detail.html', context)


@csrf_protect
def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    snippet.delete()
    messages.success(request, 'Сниппет успешно удален')
    return redirect('pages/view_snippets')

def snippet_edit(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сниппет успешно обновлен')
            return redirect('pages/view_snippets')
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'pages/edit_snippet.html', {'form': form, 'snippet': snippet})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно авторизованы')
            return redirect('view_snippets')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'pages/login.html')
    else:
        return render(request, 'pages/login.html')
    

@csrf_protect
@login_required
def my_snippets(request):
    sort = request.GET.get('sort', 'creation_date')
    if sort not in ['name', 'creation_date']:
        sort = 'creation_date'
    snippets = Snippet.objects.filter(author=request.user).order_by(sort)
    return render(request, 'pages/my_snippets.html', {'snippets': snippets})

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})

@csrf_protect
def comment_add(request, snippet_id):  
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.snippet = get_object_or_404(Snippet, id=snippet_id)  
            new_comment.save()
            return HttpResponseRedirect(f'/snippets/{snippet_id}/')  
    return HttpResponseRedirect('/some_fallback_view/')


class MyLoginView(LoginView):
    template_name = 'pages/login.html'
    success_url = '/snippets/list'