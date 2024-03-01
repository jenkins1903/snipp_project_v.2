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


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_snippets')  # Перенаправление на страницу со списком сниппетов
    else:
        form = SnippetForm()
    
    context = {'pagename': 'Добавление нового сниппета', 'form': form}
    return render(request, 'pages/add_snippet.html', context)




def snippets_page(request):
    if request.user.is_authenticated:

        snippets = Snippet.objects.filter(Q(is_public=True) | Q(author=request.user))
    else:
  
        snippets = Snippet.objects.filter(is_public=True)
    return render(request, 'pages/view_snippets.html', {'snippets': snippets})


def snippet_detail(request, id):
    snippet = get_object_or_404(Snippet, pk=id)  
    return render(request, 'pages/snippet_detail.html', {'snippet': snippet})

def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    snippet.delete()
    return redirect('view_snippets')

def snippet_edit(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect('view_snippets')  
    else:
        form = SnippetForm(instance=snippet)
    return render(request, 'pages/edit_snippet.html', {'form': form, 'snippet': snippet})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_snippets')  
        else:

            return render(request, 'pages/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'pages/login.html')
    

def my_snippets(request):

    snippets = Snippet.objects.filter(author=request.user)
    return render(request, 'pages/my_snippets.html', {'snippets': snippets})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  
    else:
        form = SignUpForm()
    return render(request, 'pages/signup.html', {'form': form})