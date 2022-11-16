from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home_page(request):
    users = User.objects.filter(hackathon_participant=True)
    count = users.count()
    users = users[0:20]
    events = Event.objects.all() 
    context = {'users':users, 'events':events, 'count':count}
    return render(request, 'home.html', context)

def event_page(request, pk):
    event = Event.objects.get(id=pk)

    registered = False
    submitted = False

    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists() 
    context = {"event":event, 'registered':registered, 'submitted': submitted}  
    return render(request, 'event.html', context)

def login_page(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
            )
        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def register_page(request):
    form = CustomUserCreateForm()
    
    if request.method == "POST":
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit =False)
            user.save()
            login(request, user)
            return redirect('home')

    page = 'register'
    context = {'page': page, 'form':form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')



def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context)

def edit_account(request):
    context = {}
    return render(request, 'user_form.html', context)




@login_required(login_url='login')
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    if request.method == "POST":
        event.participants.add(request.user)
        return redirect('event', pk=event.id)
    
    return render(request, 'event_confirmation.html', {'event': event})


@login_required(login_url='login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()

            return redirect('account')


    context = {'event': event, 'form':form }
    return render(request, 'submit_form.html', context)

#owner authentication
@login_required(login_url='login')
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse("YOU can't be here")

    event = submission.event 
    form = SubmissionForm(instance=submission)
    if request.method == "POST":
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form, 'event':event}
    return render(request, 'submit_form.html', context)