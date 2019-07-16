### Views is the most important file as it contains all function that we are going to use
## all url renders and handelled here
#


# import sys
# sys.path.append('spoor/')


import math
import datetime
import threading
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .forms import CvForm, UserForm, UserProfileForm, ResumeUpdate, ProfileUpdate
from .models import Candidate, Vacancy, JobApplicant
from django.contrib.auth.models import User
import numpy as np
from .spoor.final import main
from django.db.models.functions import TruncDay
from django.db.models import Count
from .spoor.ranking import ranking
from django.utils import timezone
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from  django.core.mail import send_mail


# Create your views here.


#this checks if user is already logged in and if not handells the login process, it is the first default function called
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        availJobs = Vacancy.objects.filter(deadline__gt=timezone.now())
        finishedJobs = Vacancy.objects.filter(deadline__lt=timezone.now())
        applicants = Applicant.objects.all()
        jobs = Vacancy.objects.all()
        now = datetime.datetime.now()
        value= Vacancy.check
        for all in finishedJobs:
            if (value =='F'):
                for k in applicants:
                    for all in jobapplicant.rank:
                        print (k.applicant.applicant)
                        print (JobApplicant.applicant)
                        if k.applicant.applicant == JobApplicant.applicant:
                            print('v.index 1')
                        else:
                            print('v. index 2')
            Job.check == 'T'



        applicant = Applicant.objects.get(applicant=request.user)

        applWithResume = []
        for i in Applicant.objects.all():
            if i.resume:
                applWithResume.append(i)


        context = {
            'user': request.user,
            'jobs': jobs,
            'availJobs': availJobs,
            'finishedJobs': finishedJobs,
            'applicants': applicants,
            'now': now,
            'applicant' : applicant,
            'applWithResume': applWithResume,
        }
        return render(request, 'home.html', context)



#this is for vacancy searching...searches in vacancy content
def search(request):
    applicant = Applicant.objects.get(applicant=request.user)
    query = request.POST.get('q', '')
    if query:
        qset = (
            Q(company__icontains=query)|
            Q(title__icontains=query)|
            Q(category__icontains=query)|
            Q(skills__icontains=query)
        )
        print(qset)

        jobs = Vacancy.objects.filter(qset)

    else:
        jobs = []
    now = timezone.now()
    return render(request, 'search.html', {'jobs': jobs, 'query': query, 'now' : now, 'applicant' : applicant})


# logging out usr....retuns to main page
def logout_user(request):
    logout(request)
    return redirect('index')


# login handelling by checking data and captcha
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        if result['success']:
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'error_message': 'Account Deactivated'})
            else:
                return render(request, 'login.html', {'error_message': 'Login Invalid'})
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')
    return render(request, 'login.html')



#register handelling and email notifier
def register(request):
    form1 = UserForm(request.POST or None, request.FILES or None)
    form2 = UserProfileForm(request.POST or None, request.FILES or None)
    if form1.is_valid() and form2.is_valid:
        user = form1.save(commit=False)
        username = form1.cleaned_data['username']
        password = form1.cleaned_data['password']
        user.set_password(password)
        user.save()

        profile = form2.save(commit=False)
        profile.applicant = user
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                profile.save()
                #send_mail(subject,message,from_email,tolist,fail_silently)
                subject = 'Thank you for joining Spoor'
                message =  '\n Welcome to Spoor!! \n Your Account has been successfully created. Please submit your Résumé to apply for vacancies. We hope you have a wonderful experience. \n We will send you further updates soon.\n\n\n-TheSpoorTeam, 2018.'
                from_email = settings.EMAIL_HOST_USER
                to_list= [user.email]
                send_mail(subject,message,from_email,to_list,fail_silently=True)
                return redirect('index')
    context = {'form1': form1, 'form2': form2}
    return render(request, 'register.html', context)


#uploading resume
def vitae(request, update):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        instance = Candidate.objects.get(applicant=request.user)
        form = CvForm(request.POST or None, request.FILES or None, instance=instance)
        print("v.vitae 1")
        print(update, bool(update))
        if form.is_valid():
            cv = form.save(commit=False)
            print("v.vitae 2")
            cv.resume = request.FILES['resume']
            file_type = cv.resume.url.split('.')[-1]
            file_type = file_type.lower()
            print(file_type)
            if file_type not in ['pdf','doc','docx']:
                context = {
                    'form': form,
                    'error_message': 'File must in PDF or doc or docx',
                }
                return render(request, 'submit_cv.html', context)
            cv.save()
            t = threading.Thread(target=populateResumetoDb, args=(request,))
            print("v. vitae processing")
            t.daemon = True
            t.start()
            return redirect('index')

        applicant = Candidate.objects.get(applicant = request.user)
        if applicant.resume:
            print("v. vitae resume 1", update, type(update))
            if update == '0':
                print("v. vitae update 0")
                resume_data = open(applicant.resume.path, 'rb').read()
                return HttpResponse(resume_data, content_type="application/pdf")
            else:
                context = {
                    'form': form,
                    'applicant': applicant
                }
                return render(request, 'submit_cv.html', context)
        else:
            print("v. vitae update 1")
            context = {
                'form': form,
                'applicant': applicant
            }
            return render(request, 'submit_cv.html', context)


#job details rendering
def details(request,id):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        applied = False
        job = Vacancy.objects.get(id=id)

        appliers = JobApplicant.objects.filter(job=job)

        byDate = JobApplicant.objects.filter(job=job).annotate(date=TruncDay('appliedAt'))
        final = byDate.values('date').annotate(appCount=Count('applicant'))
        applicant = Candidate.objects.get(applicant=request.user)
        try:
            alappliers = JobApplicant.objects.get(job=job, applicant=applicant)
            if applicant == alappliers.applicant:
                applied = True
        except:
            print("v.details exe")

        allapp = JobApplicant.objects.filter(job=job).order_by('rank')

    context = {
            'user':request.user,
            'job': job,
            'applicant' : applicant,
            'appliers': appliers,
            'applied' : applied,
            'allapp' : allapp,

        }
    return render(request, 'details.html', context)

"""
def add(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
        user = request.user
        if request.method == 'POST':
            if request.is_ajax():
                cuser = request.POST.get('cuser',False)
                if user == User.objects.get(username=cuser):
                    applied_job_id = request.POST.get('job',False)
                    applied_job = Vacancy.objects.get(id=applied_job_id)
                    applic = Applicant.objects.get(applicant=user)
                    currentStatus = JobApplicant.objects.filter(job=applied_job)
                    currentApplicants = []
                    for pp in currentStatus:
                        currentApplicants.append(pp.applicant.id)
                    if applic.id not in currentApplicants:
                        jobapplicant = JobApplicant(job=applied_job, applicant=applic)
                        t = threading.Thread(target=ranking, args=(jobapplicant, applic, applied_job))
                        print("Thread runnning")
                        t.daemon = True
                        t.start()
                    return JsonResponse({'data':applied_job_id})
                return JsonResponse({'data':"users not same"})
        return JsonResponse({'data':"not post"})



def stats(request):
    jobs = Vacancy.objects.all()
    users = Applicant.objects.all()

    x = np.arange(0,10,0.1)
    y = [math.sin(x) for x in np.arange(0,10,0.1)]

    source = ColumnDataSource(data=dict(
        x = x,
        y = y))   
    
    title = 'y = f(x)'

    hover1 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    hover2 = HoverTool(tooltips=[
        ("(x,y)","($x, $y)"),
    ])

    p1 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover1,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)
    
    p2 = figure(title = title, 
                  x_axis_label="X",
                  y_axis_label="Y", 
                  tools=[hover2,"pan,wheel_zoom,box_zoom,reset,save"],
                  plot_width=800,
                  plot_height=500,
                  responsive=False,
                  toolbar_location='below',
                  logo=None)



    p1.circle('x', 'y', line_width=2, source=source,)
    tab1 = Panel(child=p1, title='circle')

    p2.line('x', 'y', line_width=2, source=source,)
    tab2 = Panel(child=p2, title='line')

    tabs = Tabs(tabs=[tab1, tab2],)

    script, div = components(tabs)


    return render(request, 'stats.html', {'jobs':jobs, 'users':users, 'script':script, 'div':div,})
"""


#function which writes into db
def populateResumetoDb(request, ):

    user = request.user
    applicant = Candidate.objects.get(applicant = user)
    resume = applicant.resume

    extractedSkills, ontologySkill, extractedWorkExp, ontologyWorkExperience, extractedEducation, extractedCert, linksCertification = main(resume.path)
    print("extracted")

    applicant_skills = ''
    for skills in extractedSkills:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_skills += temp[:-2]+'\n'


    applicant_workExp = ''
    for skills in extractedWorkExp:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_workExp += temp[:-2] + '\n'


    applicant_certs = ''
    for skills in extractedCert:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_certs += temp[:-2] + '\n'

    link_cert = ''
    for li in linksCertification:
        link_cert += li + ' '
    link_cert = link_cert[:-1]

    applicant_Edu = ''
    for skills in extractedEducation:
        temp = ''
        for item in skills:
            temp += item + '; '
        applicant_Edu += temp[:-2] + '\n'


    applicant.applicant_Skill = applicant_skills
    applicant.skill_ontology = str(ontologySkill)
    applicant.applicant_WorkExp = applicant_workExp
    applicant.work_experience_ontology = str(ontologyWorkExperience)
    applicant.applicant_Cert = applicant_certs
    applicant.certification_link = link_cert
    applicant.applicant_Edu = applicant_Edu

    applicant.save()




#displays user dashboard
def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        cuser = request.user
        applicant = Candidate.objects.get(applicant = cuser)
        jobs_applied_remain = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__gt = timezone.now())
        jobs_applied_finished = JobApplicant.objects.filter(applicant__applicant = cuser, job__deadline__lt = timezone.now())
        for job in jobs_applied_finished:
            print(job.skillScore, job.educationScore, job.workExpScore, job.certificationScore)
        print("\n\n\n\n\n\n\n\n")
        print(applicant.applicant.username, applicant.applicant.email)
        context = {
            'jobs_applied_remain':jobs_applied_remain,
            'jobs_applied_finished':jobs_applied_finished,
            'applicant' : applicant,
        }
        return render(request, 'dashboard.html', context)
