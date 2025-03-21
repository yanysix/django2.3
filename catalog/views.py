from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *


def index(request):
    done_requests = Request.objects.filter(status='В')[:4]
    accepted_request_counter = Request.objects.filter(status='П').count()
    return render(request, 'index.html', {
        'done_requests': done_requests, 'accepted_request_counter': accepted_request_counter}
    )


@login_required
def indexacc(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'profile.html', {'user_requests': user_requests})

@login_required
def indexacc_filter(request):
    user_filter_requests = Request.objects.filter(user=request.user, status=request.GET['status'][0])
    return render(request, 'profile.html', {'user_requests': user_filter_requests})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.fio = form.cleaned_data['fio']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def request_add(request):
    if request.method == 'POST':
        form = RequestCreateForm(request.POST, request.FILES)
        if form.is_valid():
            request_save = form.save(commit=False)
            request_save.user = request.user
            request_save.save()
            return redirect('profile')
    else:
        form = RequestCreateForm(initial={'user': request.user.pk})
    return render(request, 'request_add.html', {'form': form})

@login_required
def request_delete(request, pk):
    request_obj = Request.objects.get(id=pk)
    if request_obj.status == 'Н':
        return render(request, 'request_delete_confirm.html', {'request': request_obj})

@login_required
def request_delete_confirm(request, pk):
    request = Request.objects.get(id=pk)
    request.delete()
    return redirect('profile')

@login_required
def requests(request):
    new_requests = Request.objects.filter(status='Н')
    context = {'new_requests': new_requests}
    return render(request, 'requests.html', context)

@login_required
def request_work_change(request, pk):
    request_instance = Request.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestWorkStatusChangeForm(request.POST, request.FILES, instance=request_instance)
        if form.is_valid():
            request = form.save(commit=False)
            request.status = 'П'  # Устанавливаем статус "Принято в работу"
            request.save()
            return redirect('requests')
    else:
        form = RequestWorkStatusChangeForm(initial={'status': 'A'})
    return render(request, 'request_work_change.html', {'form': form})

@login_required
def request_done_change(request, pk):
    request_instance = Request.objects.get(id=pk)
    if request.method == 'POST':
        form = RequestDoneStatusChangeForm(request.POST, request.FILES, instance=request_instance)
        if form.is_valid():
            request = form.save(commit=False)
            request.status = 'В'  # Устанавливаем статус "Выполнено"
            request.save()
            return redirect('requests')
    else:
        form = RequestDoneStatusChangeForm(initial={'status': 'D'})
    return render(request, 'request_done_change.html', {'form': form})


