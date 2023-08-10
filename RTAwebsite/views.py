import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from websets.forms import CreateUserForm
from websets.forms import audioAccept
from websets.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request): 
    context = {'Name': 'Patrick', 'conversionPage':'AIVoices'}
    return render(request, 'home.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Congratulations ' + user + '!')

                return redirect('login')  # Redirect to a success page after saving the form

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
       return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
        
            user = authenticate(request, username=username, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        
        context = {}
        return render(request, 'loginPage.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def about(request):
    return render(request, 'about.html')

def aiModels(request):
    return render(request, 'aiModel.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
       
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        print("The data has been written to the db")

    return render(request, 'contact.html')

def userAccount(request):
    return render(request, 'userAccount.html')

def conversion(request):
    if request.method == 'POST':
        form = audioAccept(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['audioFile']
            
            # Determine the path to save the uploaded file
            save_path = os.path.join(settings.MEDIA_ROOT, 'accepted_Audio')  # 'accepted_Audio' is the subdirectory where you want to save the files
            os.makedirs(save_path, exist_ok=True)  # Create the directory if it doesn't exist
            
            # Construct the full file path
            file_name = uploaded_file.name
            file_path = os.path.join(save_path, file_name)
            
            # Save the uploaded file to the desired location
            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            
            # Handle the uploaded file processing here, if needed
            
    else:
        form = audioAccept()
    
    context = {'form': form}
    return render(request, 'conversion.html', context)

