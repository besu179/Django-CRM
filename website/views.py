from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddrecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "There has been an error logging in. Please try again later.")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Registered Successfully!')
                return redirect('home')
            else:
                messages.error(request, 'There was an error logging in. Please try again.')
                return redirect('register')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.error(request, 'You must be logged in!!!')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Deleted Successfully!!!')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in!!!')
        return redirect('home')

def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddrecordForm(request.POST)
            if form.is_valid():
                add_record = form.save(commit=False)
                add_record.user = request.user
                add_record.save()
                messages.success(request, 'Record added Successfully ...')
                return redirect('home')
        else:
            form = AddrecordForm()
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You must be logged in ...')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddrecordForm(request.POST or None, instance= current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated successfully')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in!!!')
        return redirect('home')