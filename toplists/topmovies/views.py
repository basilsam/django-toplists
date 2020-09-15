import requests, json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.paginator import Paginator
from .forms import Signup, Login, Update
from topmovies.models import MovieList

def clean_response(response):
    length = len(response)
    pop_list = []
    popular_movies = {}
    for x in range(length):
        pop_list.append({"title" : response[x]['title'], "id" : response[x]['id'], "poster_path" : response[x]['poster_path']})
    popular_movies['movies'] = pop_list
    return popular_movies

def account(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
        user = User.objects.get(username=request.user)
        form = Update(username=user.username, email=user.email)
        return render(request, "topmovies_form.html", {'form' : form, 'purpose' : 'Update', 'logged_in' : True, 'user' : user})
    else:
        form = Update(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user)
            new_pass = form.cleaned_data['Password'] 
            new_email = form.cleaned_data['Email']
            if (len(new_pass) > 0):
                user.set_password(new_pass)
            if (len(new_email) > 0):
                if User.objects.filter(email=new_email).exists() and user.email != new_email:
                    return JsonResponse({'success' : False, 'purpose' : 'Update', 'reason' : 'email'})
                user.email = new_email
            user.save()
            return JsonResponse({'success' : True, 'purpose' : 'Update'})

def signup(request):
    if request.method == 'GET':
        form = Signup()
        return render(request, "topmovies_form.html", {'form' : form, 'purpose' : 'Sign up'})
    elif request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            try:
                if User.objects.filter(email=form.cleaned_data['Email']).exists():
                    return JsonResponse({'success' : False, 'purpose' : 'Sign up', 'reason' : 'email'})
                user = User.objects.create_user(form.cleaned_data['Username'], form.cleaned_data['Email'], form.cleaned_data['Password'])
                return login(request)
            except:
                return JsonResponse({'success' : False, 'purpose' : 'Sign up', 'reason' : 'username'})
        else:
            return JsonResponse({'success' : False, 'purpose' : 'Sign up', 'reason' : 'invalid'})

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('my-list'))
    if request.method == 'GET':
        form = Login()
        return render(request, "topmovies_form.html", {'form' : form, 'purpose' : 'Log in'})
    elif request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['Username'], password=form.cleaned_data['Password'])
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'success' : True, 'redirect' : reverse('my-list')})
            else:
                return JsonResponse({'success' : False, 'purpose' : 'Log in'})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
            
def popular_movies(request):
    if request.method == 'GET':
        page = request.GET.get('page', None)
        if page is None:
            return HttpResponseRedirect(reverse('popular-movies') + '?page=1')
        elif not page.isdigit() or int(page) < 1:
            raise Http404("Page does not exist")
        response = requests.get(f'https://api.themoviedb.org/3/movie/popular?api_key=566703fe3999a4c89d3ac1849624c30b&page={page}').json()['results']
        return render(request, 'topmovies_list.html', {'list': clean_response(response), 'logged_in' : request.user.is_authenticated})

def top_rated(request):
    if request.method == 'GET':
        page = request.GET.get('page', None)
        if page is None:
            return HttpResponseRedirect(reverse('top-rated') + '?page=1')
        elif not page.isdigit() or int(page) < 1:
            raise Http404("Page does not exist")
        response = requests.get(f'https://api.themoviedb.org/3/movie/top_rated?api_key=566703fe3999a4c89d3ac1849624c30b&page={page}').json()['results']
        return render(request, 'topmovies_list.html', {'list': clean_response(response), 'logged_in' : request.user.is_authenticated})

@csrf_exempt
def add_movie(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    movie_id = request.POST['movie_id']
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=566703fe3999a4c89d3ac1849624c30b').json()
    new_entry = {"title" : response['title'], "id" : response['id'], "poster_path" : response['poster_path']}
    try:
        model_obj = MovieList.objects.get(user=request.user)
        if new_entry not in model_obj.movie_list['movies']:
            model_obj.movie_list['movies'].append(new_entry)
            model_obj.save()
        else:
            return JsonResponse({'success' : False})
    except:
        movie_dict = {}
        movie_list = [new_entry]
        movie_dict['movies'] = movie_list
        user = User.objects.get(username=request.user)
        new_list = MovieList(user=user, movie_list=movie_dict)
        new_list.save()
    return JsonResponse({'success': True})

@csrf_exempt
def delete_movie(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    movie_id = request.POST['movie_id']
    model_obj = MovieList.objects.get(user=request.user)

    for entry in model_obj.movie_list['movies']:
        if entry['id'] == int(movie_id):
            model_obj.movie_list['movies'].remove(entry)
            model_obj.save()
            break
    return JsonResponse({'success': True})

def my_list(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.user)
            my_list = MovieList.objects.get(user=user).movie_list
            return render(request, 'topmovies_my_list.html', {'list': my_list, 'logged_in' : request.user.is_authenticated, 'list_size' : len(my_list['movies'])})
        except:
            return render(request, 'topmovies_my_list.html', {'list': [], 'logged_in' : request.user.is_authenticated, 'list_size' : 0})

def search(request):
    page = request.GET.get('page', None)
    title = request.GET.get('title', None)
    if title == '' or title is None :
        raise Http404("Page does not exist")
    if page is None:
        return HttpResponseRedirect(reverse('search') + f'?title={title}&page=1')
    elif not page.isdigit() or int(page) < 1:
        raise Http404("Page does not exist")
    response = requests.get(f'http://api.themoviedb.org/3/search/movie?api_key=566703fe3999a4c89d3ac1849624c30b&query={title}&page={page}').json()['results']
    return render(request, 'topmovies_list.html', {'list': clean_response(response), 'logged_in' : request.user.is_authenticated})