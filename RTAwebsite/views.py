import os
import requests, base64
from django.conf import settings
from django.shortcuts import render, redirect
from websets.forms import audioAccept, CreateUserForm
from websets.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    context = {'Name': 'Patrick', 'conversionPage': 'AIVoices'}
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

            uploaded_file_path = os.path.join(settings.MEDIA_ROOT, 'accepted_Audio')
            os.makedirs(uploaded_file_path, exist_ok=True)
            file_name = uploaded_file.name
            file_path = os.path.join(uploaded_file_path, file_name)


            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Prepare the API request
            api_url = "http://localhost:7865/run/infer_convert_batch"
            audio_data = uploaded_file.read()
            base64_audio_data = base64.b64encode(audio_data).decode('utf-8')
            payload = {
                "data": [
                    0,
                    r"/Users/patrickdail/RoyalTunes/RoyalTunesAiMobagi/media/accepted_Audio",
                    "opt",
                    {"name": "zip.zip", "data": f"data:@file/octet-stream;base64,{base64_audio_data}"},
                    0,
                    "rmvpe",
                    "hello world",
                    "logs/guanguanV1.index",
                    1,
                    3,
                    0,
                    1,
                    0.33,
                    "wav",
                ]
            }

            # Make the API request
            response = requests.post(api_url, json=payload).json()
            data = response["data"]

            context = {
                'form': form,
                'uploaded_file_name': uploaded_file.name if uploaded_file else None,
                'processed_data': data,
            }
            return render(request, 'conversion.html', context)
    else:
        form = audioAccept()

    context = {'form': form}
    return render(request, 'conversion.html', context)