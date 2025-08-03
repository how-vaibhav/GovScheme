from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from .forms import FeedbackForm, AddEmployee, Add_Scheme_Form, User_Details_Form
from .models import Feedback, Notification, Scheme, UserDetails, Application
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
import json, requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from bs4 import BeautifulSoup
from django.views.decorators.http import require_POST
# Create your views here.

#Home page view, that sends username of user and their notifications if they have logged in
def home(request):
    notifications = []

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        print("User:", request.user)
        print("Notifications:", notifications)
    return render(request, 'home.html', {'notifications': notifications})


#view for feedback submission, it requires the user to be signed in to give feedbakcs
@login_required
def feedback(request):
    scheme_id = request.GET.get('scheme_id')

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('feedback')
    else:
        form = FeedbackForm(initial={'scheme': scheme_id}) if scheme_id else FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})

#view for users to view feedbacks they sent
#if a user who is in employee group accesses this page, then they are shown all feedbacks and given an option to reply to them
@login_required
def view_feedback(request):

    scheme_filter = request.GET.get('scheme', '')  # e.g., 'BBBP', 'SBA', 'NIL' or empty
    replied_filter = request.GET.get('replied', '')  # 'yes', 'no', or empty

    
    if  request.user.groups.filter(name='Employee').exists():
        feedbacks = Feedback.objects.select_related('user').order_by("-submitted_at")
    else :
        feedbacks = Feedback.objects.filter(user=request.user).order_by("-submitted_at")

    if request.user.groups.filter(name='Employee').exists():
        feedbacks = Feedback.objects.select_related('user').order_by("-submitted_at")
    else:
        feedbacks = Feedback.objects.filter(user=request.user).order_by("-submitted_at")

    # Filter by scheme if selected
    if scheme_filter:
        feedbacks = feedbacks.filter(scheme__name=scheme_filter)

    # Filter by replied or not
    if replied_filter == 'yes':
        feedbacks = feedbacks.exclude(reply__isnull=True).exclude(reply__exact='')
    elif replied_filter == 'no':
        feedbacks = feedbacks.filter(reply__isnull=True) | feedbacks.filter(reply='')

    # Pass scheme choices to template for dropdown
    scheme_choices = [(name, name) for name in Scheme.objects.values_list('name', flat=True)]

    total_feedbacks = feedbacks.count()
    total_replied = feedbacks.exclude(reply__isnull=True).exclude(reply__exact='').count()
    total_unreplied = (feedbacks.filter(reply__isnull=True) | feedbacks.filter(reply='')).count()



    return render(request, 'feedback/viewfeedback.html',{'feedbacks': feedbacks, 'scheme_choices': scheme_choices, 'selected_scheme': scheme_filter, 'selected_replied': replied_filter, 'total_feedbacks':total_feedbacks, 'total_replied':total_replied, 'total_unreplied':total_unreplied,})


#view for login-page
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change 'home' to your home view name
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

#view for sign-in page
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def add_employee(request):
    if request.method == 'POST':
        form =AddEmployee(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username= username)
                employee_group, created = Group.objects.get_or_create(name = 'Employee')
                user.groups.add(employee_group)
                user.save()
                messages.success(request, 'Employee Added')
                return redirect('add_employee')
            except User.DoesNotExist:
                form.add_error('username', 'User with this name does not exist.')
    else:
            form = AddEmployee()
    return render(request, 'addEmployee.html', {'form': form})

@login_required
@user_passes_test(is_employee)
@login_required
def reply_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == 'POST':
        reply = request.POST.get('reply')
        feedback.reply = reply
        feedback.save()
    
        Notification.objects.create(
            user=feedback.user,
            message=f"Your feedback on {feedback.scheme} has been replied to.",
            link=f"/viewfeedbacks/#{feedback.id}"
        )

        return redirect('view_feedbacks')
    return render(request, 'feedback/reply_feedback.html', {'feedback': feedback})

@csrf_exempt
def translate_page(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get("text","")
        source = data.get("source","en")
        target = data.get("target","")

        response = requests.post("http://localhost:5000/translate", json={
            "q": text,
            "source" : source,
            "target":target,
            "format":"text"
        })

        if response.status_code == 200:
            return JsonResponse({"translatedText": response.json().get("translatedText")})
        else:
            return JsonResponse({"error": "Translation failed"}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def scheme_list(request):
    schemes = Scheme.objects.all()
    return render(request, 'scheme_list.html', {'schemes': schemes})

def scheme_detail(request, pk):
    scheme = get_object_or_404(Scheme, pk=pk)

    feedbacks = Feedback.objects.all().order_by('-submitted_at')  # get all feedback for this scheme

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.scheme = scheme
            feedback.user = request.user
            feedback.save()
            return redirect('schemesapp/scheme_detail', pk=pk)  # Redirect to avoid resubmission on refresh
    else:
        form = FeedbackForm()

    context = {
        'scheme': scheme,
        'feedbacks': feedbacks,
        'form': form,
    }
    return render(request, 'schemesapp/scheme_detail.html', context)

@login_required
@user_passes_test(is_employee)
def scheme_input(request):
    storage = messages.get_messages(request)
    storage.used = True  # Clears all messages
    if request.method == 'POST':
        form = Add_Scheme_Form(request.POST)
        if form.is_valid():
            scheme = form.save()
            messages.success(request, "Schemes Added.")
            return redirect('scheme_list')
    else:
        form = Add_Scheme_Form()    
    return render(request, 'schemesapp/add_scheme.html', {'form': form})

@login_required
def user_detail_input(request):
    try:
        details = UserDetails.objects.get(user=request.user)
        return redirect('view_user_details')  # Redirect to a view-only page if already submitted
    except UserDetails.DoesNotExist:
        if request.method == 'POST':
            form = User_Details_Form(request.POST)
            if form.is_valid():
                user_details = form.save(commit=False)
                user_details.user = request.user
                user_details.save()
                messages.success(request, "User Data Added.")
                return redirect('home')
        else:
            form = User_Details_Form()    
        return render(request, 'user_detail.html', {'form': form})

@login_required
def scheme_eligibility(request, pk):
    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')
    
    scheme = get_object_or_404(Scheme, pk=pk)

    is_eligible = scheme.is_user_eligible(details)

    return render(request, 'eligibility.html', {'details': details, 'scheme':scheme, 'is_eligible':is_eligible})

@login_required
def check_all_eligibility(request):
    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')  # Force user to fill details first

    eligible_schemes = []

    all_schemes = Scheme.objects.all()
    for scheme in all_schemes:
        if scheme.is_user_eligible(details):
            eligible_schemes.append(scheme)

    return render(request, 'eligible_schemes.html', {
        'eligible_schemes': eligible_schemes,
        'total': len(eligible_schemes),
    })

@login_required
def view_user_details(request):
    user = request.user

    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail')

    fields = [(field.verbose_name.title(), getattr(details, field.name)) for field in UserDetails._meta.fields if field.name != 'id']

    return render(request, 'view_user_details.html', {'fields': fields})

@login_required
def edit_user_details(request):
    details = UserDetails.objects.get(user=request.user)
    if request.method == 'POST':
        form = User_Details_Form(request.POST, instance=details)
        if form.is_valid():
            form.save()
            return redirect('view_user_details')
    else:
        form = User_Details_Form(instance=details)
    return render(request, 'edit_user_details.html', {'form': form})

@receiver(post_save, sender=Scheme)
def notify_users_on_new_scheme(sender, instance, created, **kwargs):
    if created:
        scheme = instance

        for user_detail in UserDetails.objects.all():
            eligible = scheme.is_user_eligible(user_detail)
            message = f"New scheme '{scheme.name}' added. You are {'eligible' if eligible else 'not eligible'}."

            Notification.objects.create(
                user=user_detail.user,  # Assuming UserDetails links to User
                message=message,
                scheme=scheme,
                is_read=False,
            )

def scrape_schemes_view(request):
    quotes_list = []

    if request.method == 'POST':
        url = "http://quotes.toscrape.com/"
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', class_='quote')

            for q in quotes:
                text = q.find('span', class_='text').get_text(strip=True)
                author = q.find('small', class_='author').get_text(strip=True)
                
                # If you want to store in DB using Scheme model, adapt fields:
                scheme, created = Scheme.objects.update_or_create(
                    name=author,  # Using author as name (just for example)
                    defaults={
                        'objective': text,  # Using quote text as objective
                        'benefits': '',  # Empty or adapt as needed
                    #  'implementing_agency': '',  # Empty or adapt
                    }
                )
                quotes_list.append({'author': author, 'quote': text})

    return render(request, 'scrape.html', {'quotes': quotes_list})


def scrape_page(request):
    return render(request, 'scrape.html', {'quotes': None})


def verhoeff_check(num):
    # Multiplication table d
    d = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,2,3,4,0,6,7,8,9,5],
        [2,3,4,0,1,7,8,9,5,6],
        [3,4,0,1,2,8,9,5,6,7],
        [4,0,1,2,3,9,5,6,7,8],
        [5,9,8,7,6,0,4,3,2,1],
        [6,5,9,8,7,1,0,4,3,2],
        [7,6,5,9,8,2,1,0,4,3],
        [8,7,6,5,9,3,2,1,0,4],
        [9,8,7,6,5,4,3,2,1,0]
    ]

    # Permutation table p
    p = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,5,7,6,2,8,3,0,9,4],
        [5,8,0,3,7,9,6,1,4,2],
        [8,9,1,6,0,4,3,5,2,7],
        [9,4,5,3,1,2,6,8,7,0],
        [4,2,8,6,5,7,3,9,0,1],
        [2,7,9,3,8,0,6,4,1,5],
        [7,0,4,6,9,1,3,2,5,8]
    ]

    # Inverse table inv
    inv = [0,4,3,2,1,5,6,7,8,9]

    c = 0
    # Reverse the number string
    num = num[::-1]
    for i, digit in enumerate(num):
        c = d[c][p[i % 8][int(digit)]]

    return c == 0

@login_required
def apply_scheme(request):

    try:
        details = UserDetails.objects.get(user=request.user)
    except UserDetails.DoesNotExist:
        return redirect('user_detail') 
    
    schemes = Scheme.objects.all()

    if request.method == 'POST':
        aadhaar = request.POST.get('aadhaar')
        scheme_id = request.POST.get('scheme')

        if not verhoeff_check(aadhaar):
            messages.error(request, "Invalid Aadhaar number.")
            return render(request, 'apply_scheme.html', {'schemes': schemes})

        if not scheme_id:
            messages.error(request, "Please select a scheme.")
            return render(request, 'apply_scheme.html', {'schemes': schemes})

        try:
            scheme = Scheme.objects.get(id=scheme_id)
        except Scheme.DoesNotExist:
            messages.error(request, "Selected scheme does not exist.")
            return render(request, 'apply_scheme.html', {'schemes': schemes})

        application = Application(user=request.user, scheme=scheme)
        application.sensitive_data = aadhaar
        application.save()

        masked_aadhaar = '********' + aadhaar[-4:]
        request.session['masked_aadhaar'] = masked_aadhaar
        request.session['scheme_name'] = scheme.name
        request.session['user_name'] = request.user.username

        return redirect('apply_success')

    return render(request, 'apply_scheme.html', {'schemes': schemes})

@login_required
def apply_success(request):
    masked_aadhaar = request.session.get('masked_aadhaar')
    scheme_name = request.session.get('scheme_name')

    if not masked_aadhaar or not scheme_name:
        # Redirect back if no session data
        return redirect('apply_scheme')

    return render(request, 'success.html', {
        'aadhaar': masked_aadhaar,
        'scheme_name': scheme_name,
    })

@login_required
@user_passes_test(is_employee)
def applications_view(request):
    status_filter = request.GET.get('status', 'all')

    if status_filter == 'pending':
        applications = Application.objects.filter(status='pending')
    elif status_filter == 'accepted':
        applications = Application.objects.filter(status='accepted')
    elif status_filter == 'rejected':
        applications = Application.objects.filter(status='rejected')
    else:
        applications = Application.objects.all()

    context = {
        'applications': applications,
        'current_filter': status_filter,
        'total_count': Application.objects.count(),
        'pending_count': Application.objects.filter(status='pending').count(),
        'accepted_count': Application.objects.filter(status='accepted').count(),
        'rejected_count': Application.objects.filter(status='rejected').count(),
    }
    return render(request, 'view_applications.html', context)

@login_required
@user_passes_test(is_employee)
@require_POST
def accept_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    application.status = 'accepted'
    application.save()

    Notification.objects.create(
        user=application.user,
        scheme=application.scheme,
        message=f"Your application for '{application.scheme.name}' has been accepted.",
        is_read=False,
    )
    
    return redirect('all_applications')


@login_required
@user_passes_test(is_employee)
@require_POST
def reject_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    application.status = 'rejected'
    application.save()

    Notification.objects.create(
        user=application.user,
        scheme=application.scheme,
        message=f"Your application for '{application.scheme.name}' has been rejected.",
        is_read=False,
    )

    return redirect('all_applications')

@login_required
@require_POST
def mark_read(request):
    notif_id = request.POST.get('notification_id')
    if not notif_id:
        return JsonResponse({'error': 'No notification id provided'}, status=400)

    try:
        notif = Notification.objects.get(id=notif_id, user=request.user)
    except Notification.DoesNotExist:
        return JsonResponse({'error': 'Notification not found'}, status=404)

    notif.is_read = True
    notif.save()
    return JsonResponse({'success': True})
