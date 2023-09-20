from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from scraper.models import University, Program
from .models import *
from django.db.models import Count
from django.db.models import Q


def index(request):
    data ={}
    if request.user.is_authenticated:
        user = request.user
        viewed_programs = Program.objects.filter(program_views__user=user)
        related_programs = Program.objects.filter(university__in=viewed_programs.values('university')).exclude(id__in=viewed_programs)
        programs_to_display = (viewed_programs | related_programs).distinct()[:9]
    else:
        programs_to_display = Program.objects.all().order_by('-program_views')[:9]

    data['programs'] = programs_to_display
    data['universities'] = University.objects.all()[:3]
    return render(request, 'index.html', data)


def about(request):
    return render(request, 'about.html')


def login_view(request):
    data = {}
    if request.method=='POST':
        print(request.POST)
        try:
            email = request.POST['email']
            password = request.POST['password']
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                data['error'] = 'Invalid credentials. Please try again.'
        except:
            data['error'] = 'Invalid credentials. Please try again.'

    return render(request, 'auth/login.html', data)


def register_view(request):
    data = {}
    if request.method=='POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            password2 = request.POST['password2']
            if password != password2:
                raise Exception('Passwords do not match.')
            
            username = email.split('@')[0]
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            login(request, user)
            return redirect('app:index')
        except Exception as e:
            data['error'] = f'Error: {e}'
    return render(request, 'auth/register.html', data)


def logout_view(request):
    if request.method=='POST':
        if request.POST.get('action') == 'logout':
            logout(request)
            return redirect('app:index')
    return render(request, 'auth/logout.html')


def account(request):
    if request.method=='POST':
        if request.POST.get('action') == 'update_profile':
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            return redirect('app:account')
    return render(request, 'account/index.html')


def account_saved_programs(request):
    data = {}
    data['programs'] = Program.objects.filter(saved_programs__user=request.user)
    return render(request, 'account/programs.html', data)


def get_programs(request):
    programs = Program.objects.all()
    if request.GET.get('q'):
        programs = programs.filter(Q(title__icontains=request.GET.get('q'))|Q(degree__icontains=request.GET.get('q')))
    if request.GET.get('degree'):
        programs = programs.filter(degree__icontains=request.GET.get('degree'))
    if request.GET.get('university'):
        programs = programs.filter(university__id=request.GET.get('university'))
    return programs


def api_save_program(request):
    try:
        print(request)
        program = Program.objects.get(id=request.GET.get('program'))
        user = request.user
        if not user.is_authenticated:
            raise Exception('You must be logged in to save programs.')
        try:
            program = saved_program.objects.get(user=user, program=program)
            program.delete()

            return JsonResponse({'message': 'Removed Successfully', 'removed':True}, status=200)
        except Exception as e:
            print(e)
            saved_program.objects.create(user=user, program=program)
            return JsonResponse({'message': 'Saved Successfully', 'saved':True}, status=200)
    except Exception as e:
        print(e)
        return JsonResponse({'message': str(e)}, status=400)



def programs_list(request):
    data = {}
    data['programs'] = get_programs(request)
    data['universities'] = University.objects.all()
    
    return render(request, 'programs.html', data)


def program_details(request, id):
    data = {}
    program = Program.objects.get(id=id)
    if request.user.is_authenticated:
        program_view = ProgramView.objects.create(program=program, user=request.user)
    else:
        program_view = ProgramView.objects.create(program=program)
    data['program'] = program
    data['university'] = program.university
    return render(request, 'program_details.html', data)


def university_list(request):
    data = {}
    data['universities'] = University.objects.all()
    return render(request, 'universities.html', data)


def university_details(request, id):
    data = {}
    data['university'] = University.objects.get(id=id)
    data['hide_university'] = True
    return render(request, 'university_details.html', data)



