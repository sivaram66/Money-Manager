
from .models import MonthlyIncome, UserExpenses
from django.contrib import messages  # Import the messaging framework
from .models import MonthlyIncome
import logging
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from .models import UserExpenses, MonthlyIncome, CategoryBudget, MonthlySavings
from django.contrib.auth import update_session_auth_hash
from django.contrib import auth, messages
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
# we use get_user_model() to dynamically reference the custom user model defined in settings.py, 
#                                    ensuring flexibility and compatibility with future changes to the user model.

from django.db.models import Sum
from datetime import datetime
from .utils import send_otp
from django.contrib.auth import get_user_model
User = get_user_model()  # Get the custom user model
# Create your views here.
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user with the provided username and password
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)  # Log the user in
            return redirect("/accounts/dashboard")  # Redirect to homepage or any other page
        else:
            # Display message if credentials are wrong
            messages.info(request, 'Invalid credentials')
            # Ensure 'login' is the name of your login page URL
            return redirect('login')

    else:
        return render(request, 'login.html')

#def register(request):

    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['confirm-password']
        email = request.POST['email']

        if password1 == password2:
            # To checkuser is already exist or not
            # User.objects refers to the Django User model's default manager, 
            #                           which is used to query the database for all user-related objects.(Here we used custom user model)
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, fullname=fullname,password=password2,email=email)
                user.save()
                print("User Created")
                return redirect('login')

    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['confirm-password']
        email = request.POST['email']

        if password1 == password2:
            # To checkuser is already exist or not
            # User.objects refers to the Django User model's default manager,
            #                           which is used to query the database for all user-related objects.(Here we used custom user model)
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                otp = send_otp(email)
                request.session['otp'] = otp
                request.session['email'] = email
                request.session['fullname'] = fullname
                request.session['username'] = username
                request.session['password'] = password1
                messages.success(request, "OTP sent to your email.")
                return redirect('validate_otp')

    return render(request, 'register.html')

def validate_otp(request):
    if request.method == 'POST':
        # Concatenating the OTP digits
        otp = ''.join([
            request.POST.get(f'otp{i}', '') for i in range(1, 7)
        ])
        user_otp = otp
        if int(user_otp) == request.session.get('otp'):
            email = request.session.get('email')
            fullname = request.session.get('fullname')
            username = request.session.get('username')
            password = request.session.get('password')

            user = User.objects.create_user(
                username=username, password=password, email=email)
            user.fullname = fullname
            user.save()

            del request.session['otp']
            del request.session['email']
            del request.session['fullname']
            del request.session['username']
            del request.session['password']

            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP.")
            return redirect('validate_otp')

    return render(request, 'validate_otp.html')

def resend_otp(request):
    email = request.session.get('email')
    if email:
        otp = send_otp(email)
        request.session['otp'] = otp
        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(request, "Unable to resend OTP. Please try again.")
    return redirect('validate_otp')

@login_required
def settings(request):
    if request.method == 'POST':
        # Debugging: Print the POST data
        print("POST data:", request.POST)

        form_type = request.POST.get('form_type')

        if form_type == 'update_username':
            # Update Username
            new_username = request.POST.get('username')
            if new_username and new_username != request.user.username:
                if User.objects.filter(username=new_username).exists():
                    messages.error(request, "Username is already taken.")
                else:
                    request.user.username = new_username
                    request.user.save()
                    messages.success(request, "Username updated successfully.")

        elif form_type == 'update_email':
            # Update Email
            new_email = request.POST.get('email')
            if new_email and new_email != request.user.email:
                if User.objects.filter(email=new_email).exists():
                    messages.error(request, "Email is already taken.")
                else:
                    request.user.email = new_email
                    request.user.save()
                    messages.success(request, "Email updated successfully.")

        elif form_type == 'change_password':
            # Change Password
            current_password = request.POST.get('current-password')
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')

            if not request.user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                # Keep the user logged in
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully.")
                redirect('logout')

        return redirect('settings')  # Redirect to the same settings page

    return render(request, 'settings.html')







def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    expenses = UserExpenses.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {'expenses': expenses, 'user': request.user})

def add_expense(request):
    if request.method == 'POST':
        # Collect the data from the POST request
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        date = request.POST.get('date')

        # Save the expense to the database
        if request.user.is_authenticated:
            expense = UserExpenses(
                user=request.user,  # Associate with the logged-in user
                name=name,
                amount=amount,
                category=category,
                date = date
            )
            expense.save()  # Save the expense to the database
        else:
            return redirect('login')

        # Redirect to expense list or another page after saving
        return redirect('/accounts/dashboard')
    else:
        return render(request, 'add_expense.html')
    
def view_expenses(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Get all expenses for the logged-in user
    expenses = UserExpenses.objects.filter(user=request.user).order_by('-date')

    # Apply filters if they exist
    month = request.GET.get('month', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    current_year = datetime.now().year

    if month:
        expenses = expenses.filter(date__month=month, date__year=current_year)

    if category:
        expenses = expenses.filter(category=category)

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    # Render the expenses (filtered or not) to the template
    return render(request, 'view_expenses.html', {'expenses': expenses})


@login_required
def manage_budget(request):
    user = request.user

    # Get the current month and year
    now = datetime.now()
    current_year, current_month = now.year, now.month

    # Initialize selected year and month to current by default
    year, month = current_year, current_month

    if request.method == "POST":
        # Process the form submission
        selected_month = request.POST.get("month_year", None)
        if selected_month:
            year, month = map(int, selected_month.split('-'))

        # Handle form submission for income
        income_str = request.POST.get("income", "0")
        income = float(income_str) if income_str else 0

        income_entry = MonthlyIncome.objects.filter(
            user=user, month=month, year=year).first()
        if income_entry:
            messages.warning(
                request, "Income for this month and year already exists.")
        else:
            MonthlyIncome.objects.create(
                user=user, month=month, year=year, income=income)
            messages.success(request, "Income saved successfully.")

        return redirect("manage_budget")

    elif request.method == "GET":
        # Handle month switch via GET requests using query parameters
        selected_month = request.GET.get("month_year", None)
        if selected_month:
            year, month = map(int, selected_month.split('-'))

    # Retrieve income for the selected month
    income_entry = MonthlyIncome.objects.filter(
        user=user, month=month, year=year).first()
    total_income = income_entry.income if income_entry else 0

    # Retrieve total expenses for the selected month
    total_expenses = UserExpenses.objects.filter(
        user=user, date__year=year, date__month=month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate savings
    total_savings = total_income - total_expenses
    months_dict = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'
    }
    
    month_name = months_dict.get(month, 'Unknown')
    context = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_savings": total_savings,
        # Format month for <input type="month">
        "month": f"{year}-{str(month).zfill(2)}",
        "current_year": year,
        "current_month": month_name,
    }

    return render(request, "budget.html", context)



@login_required
def dashboard(request):
    # Get the current user
    user = request.user

    # Get the current month and year
    today = datetime.now()
    current_month = today.month
    current_year = today.year

    # Calculate total expenses for the current month
    total_expenses = UserExpenses.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0  # Default to 0 if no expenses

    # Get the monthly income for the current month
    monthly_income = MonthlyIncome.objects.filter(
        user=user,
        month=current_month,
        year=current_year
    ).first()
    # Default to 0 if no income
    monthly_income_amount = monthly_income.income if monthly_income else 0

    # Get monthly expenses for the current month
    monthly_expenses = total_expenses

    # Calculate savings (monthly savings or calculated from income and expenses)
    monthly_savings = MonthlySavings.objects.filter(
        user=user,
        month=current_month,
        year=current_year
    ).first()

    # If no savings record exists, calculate savings from income - expenses
    # if monthly_savings:
    #     savings = monthly_savings.savings
    # else:
    savings = monthly_income_amount - monthly_expenses

    # Ensure savings are not negative
    savings = max(savings, 0)  # If savings is negative, set it to 0
    

    

    # Get recent expenses (5 most recent)
    recent_expenses = UserExpenses.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year
    ).order_by('-date')[:5]

    context = {
        'monthly_income': monthly_income_amount,  # Monthly Income
        'monthly_expenses': monthly_expenses,  # Total Expenses for the Month
        'monthly_savings': savings,  # Monthly Savings
        'current_month': today.strftime('%B'),  # Get the full month name
        'current_year': current_year,
        'recent_expenses': recent_expenses,  # Add recent expenses to context
    }

    return render(request, 'dashboard.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')

def reports(requset):
    return render(requset, 'reports.html')